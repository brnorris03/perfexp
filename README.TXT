Directory organization:
-----------------------

src/
 |_ analysis/            
    |_ metrics/
    |_ tools/
 |_ examples/
    |_ drivers/
    |_ models/
 |_ me/
    |_ platforms/
    |_ tools/
 |_ storage/
    |_ tools/
 |_ util/
 |_ vis/
    |_ tools/


Installing
==========

Installation is optional (scripts will work from the source directories). To install:

    python setup.py install

To install in an alternate location:

    python setup.py install --prefix=/path/to/insallation/dir

Running
=======

Usage: 
    perfexp <drivermodule>

The driver module is a Python module in your Python path. Some examples are included in the examples/drivers directory. You can try them with:
    perfexp examples.drivers.ExperimentDriver
    perfexp examples.drivers.DataManagerDriver
    perfexp examples.drivers.AnalysisDriver
    perfexp examples.drivers.ModelDriver

You may need to adjust the examples/params.py file settings for the above examples to work.
