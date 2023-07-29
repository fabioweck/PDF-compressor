# PDF-compressor
PDF compressor with a graphical user interface (GUI)

This mini project makes use of python and PYSimpleGUI to create an interface to the user in order to compress PDF files.
The code checks if file and folder paths exist and then gives the CompressPDF class the required attributes to instantiate a new object.
Once the user clicks on 'Compress', the main function is called and performs two tasks.
Anytime the user tries to enter invalid paths, he or she will gets a popup notification to verify the fields.
The first one is instantiating a new PdfReader() object (provided by PyPDF2 module) to read the content of the file.
Along with that, a new PdfWriter() is also instantiated. With a 'for loop', the pages of the file are compressed with the method 'compress_content_streams()',
and are added to the 'writer' object, following the final step which is creating and writing a new file with the writer object.
There is a 'statistics page' displayed to the user as well, after the compression task. It shows the amount of megabytes reduced and its percentage.
In the very first beginning of the code, you can notice a function called 'make_dpi_aware'. It improves the window resolution and reduces the window/letters blur.

I hope you enjoy my program!
