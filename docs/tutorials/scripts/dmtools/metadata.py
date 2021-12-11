# metadata.py
import dmtools

image = dmtools.read_png('checks_10.png')
dmtools.write_netpbm(image, 1, 'checks_10_default_metadata.pbm')

metadata = dmtools.Metadata(author="Me",
                            title="Checks 10",
                            description="Metadata in dmtools example",
                            copyright="MIT License",
                            software="dmtools",
                            disclaimer="None",
                            warning="None",
                            comment="An insightful comment")

dmtools.write_netpbm(image, 1, 'checks_10_custom_metadata.pbm',
                     metadata=metadata)