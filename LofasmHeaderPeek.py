from lofasm.bbx import bbx

lofasmFilePath = raw_input("Please type a path to your file. ")
lofasmFileObj = bbx.LofasmFile(lofasmFilePath)
lofasmFileHeader = lofasmFileObj.header
print lofasmFileHeader
