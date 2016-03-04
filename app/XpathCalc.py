from lxml import etree
def xpathCalc(xmlfile):
    data = open('D:\\workspace\\corejava\\Shreddingtry\\app\\static\\xslt\\xpath.xlst')
    xslt_content = data.read()
    xslt_root = etree.XML(xslt_content)
    dom = etree.parse('D:\\workspace\\corejava\\Shreddingtry\\app\\static\\xml\\' + xmlfile)
    transform = etree.XSLT(xslt_root)
    result = transform(dom)
#     f = open('D:\\workspace\\corejava\\XpathSample\\app\\out1.csv', 'w')
#     f.write("Xpath \t\t\t\t Value \n")
#     f.write(str(result))
#     f.close()
    results = str(result)
    return results
