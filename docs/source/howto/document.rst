General Document
================


General preconditions:

.. code-block:: python

    import sys
    import ezdxf

    try:
        doc = ezdxf.readfile("your_dxf_file.dxf")
    except IOError:
        print(f'Not a DXF file or a generic I/O error.')
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f'Invalid or corrupted DXF file.')
        sys.exit(2)
    msp = doc.modelspace()

This works well with DXF files from trusted sources like AutoCAD or BricsCAD,
for loading DXF files with minor or major flaws look at the
:mod:`ezdxf.recover` module.

Load DXF Files with Structure Errors
------------------------------------

If you know the files you will process have most likely minor or major flaws,
use the :mod:`ezdxf.recover` module:

.. code-block:: Python

    import sys
    from ezdxf import recover

    try:  # low level structure repair:
        doc, auditor = recover.readfile(name)
    except IOError:
        print(f'Not a DXF file or a generic I/O error.')
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f'Invalid or corrupted DXF file: {name}.')
        sys.exit(2)

    # DXF file can still have unrecoverable errors, but this is maybe
    # just a problem when saving the recovered DXF file.
    if auditor.has_errors:
        print(f'Found unrecoverable errors in DXF file: {name}.')
        auditor.print_error_report()

For more loading scenarios follow the link: :mod:`ezdxf.recover`

.. _set/get header variables:

Set/Get Header Variables
------------------------

`ezdxf` has an interface to get and set HEADER variables:

.. code-block:: python

    doc.header['VarName'] = value
    value = doc.header['VarName']

.. seealso:: :class:`HeaderSection` and online documentation from Autodesk for available `header variables`_.

.. _set drawing units:

Set DXF Drawing Units
---------------------

The header variable $INSUNITS defines the drawing units for the modelspace and
therefore for the DXF document if no further settings are applied. The most
common units are 6 for meters and 1 for inches.

Use this HEADER variables to setup the default units for CAD applications
opening the DXF file. This setting is not relevant for `ezdxf` API calls,
which are unitless for length values and coordinates and decimal degrees for
angles (in most cases).

Sets drawing units:

.. code-block:: python


    doc.header['$INSUNITS'] = 6

For more information see section :ref:`DXF Units`.

Create More Readable DXF Files (DXF Pretty Printer)
---------------------------------------------------

DXF files are plain text files, you can open this files with every text editor which handles bigger files.
But it is not really easy to get quick the information you want.

Create a more readable HTML file (DXF Pretty Printer):

.. code-block::

    # on Windows
    py -3 -m ezdxf.pp your_dxf_file.dxf

    # on Linux/Mac
    python3 -m ezdxf.pp your_dxf_file.dxf

This produces a HTML file `your_dxf_file.html` with a nicer layout than a plain DXF file and DXF handles as links
between DXF entities, this simplifies the navigation between the DXF entities.

.. versionchanged:: 0.8.3

    Since ezdxf `v0.8.3 <https://ezdxf.mozman.at/release-v0-8-3.html>`_, a script called ``dxfpp`` will be added
    to your Python script path:

.. code-block:: none

    usage: dxfpp [-h] [-o] [-r] [-x] [-l] FILE [FILE ...]

    positional arguments:
      FILE             DXF files pretty print

    optional arguments:
      -h, --help       show this help message and exit
      -o, --open       open generated HTML file with the default web browser
      -r, --raw        raw mode - just print tags, no DXF structure interpretation
      -x, --nocompile  don't compile points coordinates into single tags (only in
                       raw mode)
      -l, --legacy     legacy mode - reorders DXF point coordinates


.. important:: This does not render the graphical content of the DXF file to a HTML canvas element.

Set Initial View/Zoom for the Modelspace
----------------------------------------

To show an arbitrary location of the modelspace centered in the CAD application window, set the ``'*Active'`` VPORT to
this location. The DXF attribute :attr:`dxf.center` defines the location in the modelspace, and the :attr:`dxf.height`
specifies the area of the modelspace to view. Shortcut function:

.. code-block:: Python

    doc.set_modelspace_vport(height=10, center=(10, 10))

.. _header variables: http://help.autodesk.com/view/OARX/2018/ENU/?guid=GUID-A85E8E67-27CD-4C59-BE61-4DC9FADBE74A