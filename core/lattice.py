import logging
from core.matrix import *
from core.lll import lll_reduction
from core.norms import euclidean_norm


class Lattice:

    def __init__(self, matrix):
        self.matrix = Matrix(matrix)

    @property
    def center_density(self):
        # logging.info('Calculating center density of \n' + str(self))
        b = Matrix(lll_reduction(self.matrix, .75))  # LLL basis reduction
        # logging.debug('LLL reduced matrix: \n' + str(b))
        # b = [[2261337070362461927454409267102922016, 2786201470971518444733667209602978520, -4063137902647177185063144484695148536, -2671959977702871335511367439824858800, 531672722663545453899956709733136784, -11066285142314948047878309605319720, 27810585035274635766780802193736, 80477592476538094337833811509248000, -1086760859784102657122293398528000, 9752254479710833049833929818112000, 9747833549555398956714000626688000, -51587604063166080587210730086400000, -60524907661568022921499268505600000, -492200319343401593562465996005376000, 583462545454901183949295133442048000], [-899494188371811636420443028386860751295, -1108434625918842986975056473301497593175, 1615769677917180582267507871877690824470, 1063379506967919084269378312198014464750, -211564555755008400078692722238064433455, 4403463552145413177657728884859128425, -11066285142314948047878309605319720, -32003324972857913192572676601692160000, 418985478692327218883000558146560000, -3840815241769921138963494739653120000, -3839262916845861056057412820515840000, 20325827699389244764010216109312000000, 23839618579450476114878719213455360000, 196079568186737020563995814905333760000, -232024106053219870646151905362268160000], [43100299379683388889025306183843867615329, 53169099307165431861888597272242091941905, -77270457311786540396305318689886221189234, -51146681589945024535858232882889736308450, 10165649632268733478209358027269080213121, -211564555755008400078692722238064433455, 531672722663545453899956709733136784, 1530560239010093486735522955513741312000, -15851279489922542611520014844178432000, 170593780024180617058405787354500608000, 170581396709595165194156236181655552000, -905426580732699462975835833557145600000, -1059633711003548915688215664111605760000, -9499470687531140177304292383099869184000, 11096561732823177778832541427474624512000], [-210846862850656692460971283486127288794050, -262755519394180862834491203449237567567250, 370245689432997527217142649947144030761300, 259921835205938196981636999480683713102500, -51146681589945024535858232882889736308450, 1063379506967919084269378312198014464750, -2671959977702871335511367439824858800, -7343390920768507626233985969264230400000, 15433380772089999495294136579430400000, -166762717036890406752492126544665600000, -166751881626298859537055537361766400000, 885152340637373384292412828177920000000, 1035854617331760007596258444166656000000, 51678346405920014039159918494110412800000, -53239584175571680290196398277165670400000], [-368106481519924773904534414350886532772066, -446691286081632524832614881103596134385770, 723129597447356174884835729247351174805836, 370245689432997527217142649947144030761300, -77270457311786540396305318689886221189234, 1615769677917180582267507871877690824470, -4063137902647177185063144484695148536, -13994397828070648025765945501897883648000, -5829319061605845730998746597667843072000, -6011525998430165632182239817015155712000, -6011515158598643929532710107903065088000, 37414913485358908516602361642287206400000, 37565624699356893541848541546814361600000, 45834085077100561926156783103565746176000, -101459384253512198186803104888759656448000], [200016301500560260910831484790674354345345, 338734329471008175012037829217871929160425, -446691286081632524832614881103596134385770, -262755519394180862834491203449237567567250, 53169099307165431861888597272242091941905, -1108434625918842986975056473301497593175, 2786201470971518444733667209602978520, 8181567146312233886267482488147394560000, 5828901162888013187882520719403095040000, 6015357061417455842488153477824990720000, 6015344673681940235189810806722954240000, -37435187725454234595285784647666432000000, 4785059293227585030885560693160560640000, -46029672444967955545127216452475074560000, 59316361810763695675439248039068610560000], [6619003582329282486339386856031961088000, 8181567146312233886267482488147394560000, -13994397828070648025765945501897883648000, -7343390920768507626233985969264230400000, 1530560239010093486735522955513741312000, -32003324972857913192572676601692160000, 80477592476538094337833811509248000, 347488319211581183983156828569600000000, -403086450285434173420461921140736000000, -403086450285434173420461921140736000000, -403086450285434173420461921140736000000, -403086450285434173420461921140736000000, -403086450285434173420461921140736000000, -403086450285434173420461921140736000000, 2519290314283963583877887007129600000000], [240758424397864669688220786069151921658721, 200016301500560260910831484790674354345345, -368106481519924773904534414350886532772066, -210846862850656692460971283486127288794050, 43100299379683388889025306183843867615329, -899494188371811636420443028386860751295, 2261337070362461927454409267102922016, 6619003582329282486339386856031961088000, 5845171427856628057712923734805420032000, 5840922466151505304290784195730836992000, 5840924014055499208939597157720782848000, 5865027769234121593280120861919897600000, -36505930463445683058137404383434250240000, -36334122189250078347258928254469871616000, 47987775971887298025960554706231717888000], [5845171427856628057712923734805420032000, 5828901162888013187882520719403095040000, -5829319061605845730998746597667843072000, 15433380772089999495294136579430400000, -15851279489922542611520014844178432000, 418985478692327218883000558146560000, -1086760859784102657122293398528000, -403086450285434173420461921140736000000, 18264854778558735983114680801689600000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000], [5840922466151505304290784195730836992000, 6015357061417455842488153477824990720000, -6011525998430165632182239817015155712000, -166762717036890406752492126544665600000, 170593780024180617058405787354500608000, -3840815241769921138963494739653120000, 9752254479710833049833929818112000, -403086450285434173420461921140736000000, -2922376764569397757298348928270336000000, 18264854778558735983114680801689600000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000], [5840924014055499208939597157720782848000, 6015344673681940235189810806722954240000, -6011515158598643929532710107903065088000, -166751881626298859537055537361766400000, 170581396709595165194156236181655552000, -3839262916845861056057412820515840000, 9747833549555398956714000626688000, -403086450285434173420461921140736000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, 18264854778558735983114680801689600000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000], [5865027769234121593280120861919897600000, -37435187725454234595285784647666432000000, 37414913485358908516602361642287206400000, 885152340637373384292412828177920000000, -905426580732699462975835833557145600000, 20325827699389244764010216109312000000, -51587604063166080587210730086400000, -403086450285434173420461921140736000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, 18264854778558735983114680801689600000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000], [-36505930463445683058137404383434250240000, 4785059293227585030885560693160560640000, 37565624699356893541848541546814361600000, 1035854617331760007596258444166656000000, -1059633711003548915688215664111605760000, 23839618579450476114878719213455360000, -60524907661568022921499268505600000, -403086450285434173420461921140736000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, 18264854778558735983114680801689600000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000], [-36334122189250078347258928254469871616000, -46029672444967955545127216452475074560000, 45834085077100561926156783103565746176000, 51678346405920014039159918494110412800000, -9499470687531140177304292383099869184000, 196079568186737020563995814905333760000, -492200319343401593562465996005376000, -403086450285434173420461921140736000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, 18264854778558735983114680801689600000000, -2922376764569397757298348928270336000000], [47987775971887298025960554706231717888000, 59316361810763695675439248039068610560000, -101459384253512198186803104888759656448000, -53239584175571680290196398277165670400000, 11096561732823177778832541427474624512000, -232024106053219870646151905362268160000, 583462545454901183949295133442048000, 2519290314283963583877887007129600000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, -2922376764569397757298348928270336000000, 18264854778558735983114680801689600000000]]
        # b = [list(map(Rational, x)) for x in b]
        b = Matrix(b)
        r = euclidean_norm(b[0]) / 2  # radius
        d = len(self.matrix[0])  # dimension
        bb = b * b.transpose()
        # logging.debug('Calculating determinant to get center density.')
        det_bb = bb.determinant()
        # logging.debug('determinant: ' + str(det_bb))
        # print(det_bb)
        det_bb **= .5
        # logging.debug('sqr root of det:' + str(det_bb) + str(type(det_bb)))
        # logging.debug('type r**d: ' + str(type(r**d)))
        # logging.debug(str(r**d / det_bb))
        return float(r ** d / det_bb)

    def __repr__(self):
        return str(self.matrix)

    def __str__(self):
        return str(self.matrix)


if __name__ == '__main__':
    print(1/(4*(2**.5)))
    L = Lattice([[1, 1, 1], [-1, 0, 2], [3, 5, 6]])
    print(float(L.center_density))
    # R_i = D * 1.1
    L = Lattice([[-0.0433884297520686, 0.9566115702479883, 0.0216942148760343], [0.9783057851239667, -0.02169421487603307, 0.9132231404958682], [-0.9783057851239669, 0.02169421487603307, 1.8915289256198347]])
    # R_i = D * 2
    print(float(L.center_density))
    L = Lattice([[-0.18749999999999992, 0.875, 0.09374999999999983], [0.8229166666666899, -0.09375000000000266, 0.8541666666666909], [-0.9270833333333333, 0.09375, 1.5729166666666665]])
    print(float(L.center_density))
    # R_i = D * 5
    L = Lattice([[-0.13499999999999995, 0.875, -0.09000000000000008], [0.8333333333333451, -0.1200000000000017, 0.8333333333333451], [-0.9166666666666666, 0.12, 1.5833333333333333]])
    print(float(L.center_density))
    # R_i = D * 8
    L = Lattice([[-0.12890624999999994, 0.875, -0.11132812500000011], [0.8333333333333214, -0.12304687499999825, 0.8333333333333214], [-0.9166666666666666, 0.123046875, 1.5833333333333333]])
    print(float(L.center_density))

