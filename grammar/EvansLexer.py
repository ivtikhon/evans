# Generated from grammar/Evans.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2E")
        buf.write("\u01d1\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\3\2\3\2\3\3\3\3\3\4\3")
        buf.write("\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13")
        buf.write("\3\13\3\13\3\f\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3\16\3\17")
        buf.write("\3\17\3\17\3\20\3\20\3\21\3\21\3\22\3\22\3\23\3\23\3\24")
        buf.write("\3\24\3\25\3\25\3\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31")
        buf.write("\3\32\3\32\3\32\3\33\3\33\3\33\3\34\3\34\3\34\3\35\3\35")
        buf.write("\3\35\3\36\3\36\3\36\3\37\3\37\3\37\3 \3 \3!\3!\3!\7!")
        buf.write("\u00de\n!\f!\16!\u00e1\13!\3!\3!\3!\3!\7!\u00e7\n!\f!")
        buf.write("\16!\u00ea\13!\3!\5!\u00ed\n!\3\"\3\"\3\"\3#\6#\u00f3")
        buf.write("\n#\r#\16#\u00f4\3$\6$\u00f8\n$\r$\16$\u00f9\3$\3$\6$")
        buf.write("\u00fe\n$\r$\16$\u00ff\3$\5$\u0103\n$\3$\3$\6$\u0107\n")
        buf.write("$\r$\16$\u0108\3$\5$\u010c\n$\3$\6$\u010f\n$\r$\16$\u0110")
        buf.write("\3$\3$\5$\u0115\n$\3%\3%\3%\3%\3%\3%\3%\3%\3%\5%\u0120")
        buf.write("\n%\3&\3&\5&\u0124\n&\3&\6&\u0127\n&\r&\16&\u0128\3\'")
        buf.write("\3\'\3\'\3\'\3\'\3\'\3(\3(\3(\3(\3(\3)\3)\3)\3)\3)\3)")
        buf.write("\3*\3*\3*\3*\3*\3+\3+\3+\3+\3+\3,\3,\3,\3,\3,\3-\3-\3")
        buf.write("-\3.\3.\3.\3.\3.\3/\3/\3/\3/\3/\3\60\3\60\3\60\3\60\3")
        buf.write("\61\3\61\3\61\3\61\3\61\3\61\3\62\3\62\3\62\3\62\3\63")
        buf.write("\3\63\3\63\3\63\3\63\3\63\3\64\3\64\3\64\3\64\3\64\3\65")
        buf.write("\3\65\3\65\3\65\3\65\3\66\3\66\3\66\3\66\3\67\3\67\3\67")
        buf.write("\3\67\3\67\38\38\38\38\38\39\39\39\39\39\3:\3:\3:\3:\3")
        buf.write(":\3;\3;\3;\3<\3<\3<\3<\3<\3=\3=\3=\3=\3=\3>\3>\3>\3>\3")
        buf.write("?\3?\3?\3?\3?\3?\3@\3@\3@\3@\3A\3A\3A\3A\3B\3B\3B\3B\3")
        buf.write("C\3C\3C\3C\3D\3D\3D\3D\7D\u01b9\nD\fD\16D\u01bc\13D\3")
        buf.write("E\3E\3F\3F\3G\3G\7G\u01c4\nG\fG\16G\u01c7\13G\3G\3G\3")
        buf.write("H\6H\u01cc\nH\rH\16H\u01cd\3H\3H\2\2I\3\3\5\4\7\5\t\6")
        buf.write("\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20")
        buf.write("\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65")
        buf.write("\34\67\359\36;\37= ?!A\"C\2E#G$I%K\2M&O\'Q(S)U*W+Y,[-")
        buf.write("]._/a\60c\61e\62g\63i\64k\65m\66o\67q8s9u:w;y<{=}>\177")
        buf.write("?\u0081@\u0083A\u0085B\u0087C\u0089\2\u008b\2\u008dD\u008f")
        buf.write("E\3\2\13\4\2$$^^\4\2))^^\n\2$$))^^ddhhppttvv\4\2GGgg\4")
        buf.write("\2--//\4\2C\\c|\3\2\62;\4\2\f\f\16\17\5\2\13\f\17\17\"")
        buf.write("\"\2\u01e2\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2")
        buf.write("\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2")
        buf.write("\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2")
        buf.write("\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#")
        buf.write("\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2")
        buf.write("\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65")
        buf.write("\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2")
        buf.write("\2?\3\2\2\2\2A\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2")
        buf.write("\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2")
        buf.write("\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3")
        buf.write("\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i")
        buf.write("\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2")
        buf.write("s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2")
        buf.write("\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2")
        buf.write("\2\2\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u008d\3\2\2\2\2")
        buf.write("\u008f\3\2\2\2\3\u0091\3\2\2\2\5\u0093\3\2\2\2\7\u0095")
        buf.write("\3\2\2\2\t\u0097\3\2\2\2\13\u0099\3\2\2\2\r\u009b\3\2")
        buf.write("\2\2\17\u009d\3\2\2\2\21\u009f\3\2\2\2\23\u00a1\3\2\2")
        buf.write("\2\25\u00a3\3\2\2\2\27\u00a6\3\2\2\2\31\u00a9\3\2\2\2")
        buf.write("\33\u00ac\3\2\2\2\35\u00af\3\2\2\2\37\u00b2\3\2\2\2!\u00b4")
        buf.write("\3\2\2\2#\u00b6\3\2\2\2%\u00b8\3\2\2\2\'\u00ba\3\2\2\2")
        buf.write(")\u00bc\3\2\2\2+\u00be\3\2\2\2-\u00c0\3\2\2\2/\u00c2\3")
        buf.write("\2\2\2\61\u00c4\3\2\2\2\63\u00c6\3\2\2\2\65\u00c9\3\2")
        buf.write("\2\2\67\u00cc\3\2\2\29\u00cf\3\2\2\2;\u00d2\3\2\2\2=\u00d5")
        buf.write("\3\2\2\2?\u00d8\3\2\2\2A\u00ec\3\2\2\2C\u00ee\3\2\2\2")
        buf.write("E\u00f2\3\2\2\2G\u0114\3\2\2\2I\u011f\3\2\2\2K\u0121\3")
        buf.write("\2\2\2M\u012a\3\2\2\2O\u0130\3\2\2\2Q\u0135\3\2\2\2S\u013b")
        buf.write("\3\2\2\2U\u0140\3\2\2\2W\u0145\3\2\2\2Y\u014a\3\2\2\2")
        buf.write("[\u014d\3\2\2\2]\u0152\3\2\2\2_\u0157\3\2\2\2a\u015b\3")
        buf.write("\2\2\2c\u0161\3\2\2\2e\u0165\3\2\2\2g\u016b\3\2\2\2i\u0170")
        buf.write("\3\2\2\2k\u0175\3\2\2\2m\u0179\3\2\2\2o\u017e\3\2\2\2")
        buf.write("q\u0183\3\2\2\2s\u0188\3\2\2\2u\u018d\3\2\2\2w\u0190\3")
        buf.write("\2\2\2y\u0195\3\2\2\2{\u019a\3\2\2\2}\u019e\3\2\2\2\177")
        buf.write("\u01a4\3\2\2\2\u0081\u01a8\3\2\2\2\u0083\u01ac\3\2\2\2")
        buf.write("\u0085\u01b0\3\2\2\2\u0087\u01b4\3\2\2\2\u0089\u01bd\3")
        buf.write("\2\2\2\u008b\u01bf\3\2\2\2\u008d\u01c1\3\2\2\2\u008f\u01cb")
        buf.write("\3\2\2\2\u0091\u0092\7}\2\2\u0092\4\3\2\2\2\u0093\u0094")
        buf.write("\7\177\2\2\u0094\6\3\2\2\2\u0095\u0096\7<\2\2\u0096\b")
        buf.write("\3\2\2\2\u0097\u0098\7*\2\2\u0098\n\3\2\2\2\u0099\u009a")
        buf.write("\7+\2\2\u009a\f\3\2\2\2\u009b\u009c\7.\2\2\u009c\16\3")
        buf.write("\2\2\2\u009d\u009e\7?\2\2\u009e\20\3\2\2\2\u009f\u00a0")
        buf.write("\7=\2\2\u00a0\22\3\2\2\2\u00a1\u00a2\7\60\2\2\u00a2\24")
        buf.write("\3\2\2\2\u00a3\u00a4\7-\2\2\u00a4\u00a5\7?\2\2\u00a5\26")
        buf.write("\3\2\2\2\u00a6\u00a7\7/\2\2\u00a7\u00a8\7?\2\2\u00a8\30")
        buf.write("\3\2\2\2\u00a9\u00aa\7,\2\2\u00aa\u00ab\7?\2\2\u00ab\32")
        buf.write("\3\2\2\2\u00ac\u00ad\7\61\2\2\u00ad\u00ae\7?\2\2\u00ae")
        buf.write("\34\3\2\2\2\u00af\u00b0\7\'\2\2\u00b0\u00b1\7?\2\2\u00b1")
        buf.write("\36\3\2\2\2\u00b2\u00b3\7]\2\2\u00b3 \3\2\2\2\u00b4\u00b5")
        buf.write("\7_\2\2\u00b5\"\3\2\2\2\u00b6\u00b7\7#\2\2\u00b7$\3\2")
        buf.write("\2\2\u00b8\u00b9\7-\2\2\u00b9&\3\2\2\2\u00ba\u00bb\7/")
        buf.write("\2\2\u00bb(\3\2\2\2\u00bc\u00bd\7,\2\2\u00bd*\3\2\2\2")
        buf.write("\u00be\u00bf\7\61\2\2\u00bf,\3\2\2\2\u00c0\u00c1\7\'\2")
        buf.write("\2\u00c1.\3\2\2\2\u00c2\u00c3\7>\2\2\u00c3\60\3\2\2\2")
        buf.write("\u00c4\u00c5\7@\2\2\u00c5\62\3\2\2\2\u00c6\u00c7\7>\2")
        buf.write("\2\u00c7\u00c8\7?\2\2\u00c8\64\3\2\2\2\u00c9\u00ca\7@")
        buf.write("\2\2\u00ca\u00cb\7?\2\2\u00cb\66\3\2\2\2\u00cc\u00cd\7")
        buf.write("#\2\2\u00cd\u00ce\7?\2\2\u00ce8\3\2\2\2\u00cf\u00d0\7")
        buf.write("?\2\2\u00d0\u00d1\7?\2\2\u00d1:\3\2\2\2\u00d2\u00d3\7")
        buf.write("(\2\2\u00d3\u00d4\7(\2\2\u00d4<\3\2\2\2\u00d5\u00d6\7")
        buf.write("~\2\2\u00d6\u00d7\7~\2\2\u00d7>\3\2\2\2\u00d8\u00d9\7")
        buf.write("A\2\2\u00d9@\3\2\2\2\u00da\u00df\7$\2\2\u00db\u00de\5")
        buf.write("C\"\2\u00dc\u00de\n\2\2\2\u00dd\u00db\3\2\2\2\u00dd\u00dc")
        buf.write("\3\2\2\2\u00de\u00e1\3\2\2\2\u00df\u00dd\3\2\2\2\u00df")
        buf.write("\u00e0\3\2\2\2\u00e0\u00e2\3\2\2\2\u00e1\u00df\3\2\2\2")
        buf.write("\u00e2\u00ed\7$\2\2\u00e3\u00e8\7)\2\2\u00e4\u00e7\5C")
        buf.write("\"\2\u00e5\u00e7\n\3\2\2\u00e6\u00e4\3\2\2\2\u00e6\u00e5")
        buf.write("\3\2\2\2\u00e7\u00ea\3\2\2\2\u00e8\u00e6\3\2\2\2\u00e8")
        buf.write("\u00e9\3\2\2\2\u00e9\u00eb\3\2\2\2\u00ea\u00e8\3\2\2\2")
        buf.write("\u00eb\u00ed\7)\2\2\u00ec\u00da\3\2\2\2\u00ec\u00e3\3")
        buf.write("\2\2\2\u00edB\3\2\2\2\u00ee\u00ef\7^\2\2\u00ef\u00f0\t")
        buf.write("\4\2\2\u00f0D\3\2\2\2\u00f1\u00f3\5\u008bF\2\u00f2\u00f1")
        buf.write("\3\2\2\2\u00f3\u00f4\3\2\2\2\u00f4\u00f2\3\2\2\2\u00f4")
        buf.write("\u00f5\3\2\2\2\u00f5F\3\2\2\2\u00f6\u00f8\5\u008bF\2\u00f7")
        buf.write("\u00f6\3\2\2\2\u00f8\u00f9\3\2\2\2\u00f9\u00f7\3\2\2\2")
        buf.write("\u00f9\u00fa\3\2\2\2\u00fa\u00fb\3\2\2\2\u00fb\u00fd\7")
        buf.write("\60\2\2\u00fc\u00fe\5\u008bF\2\u00fd\u00fc\3\2\2\2\u00fe")
        buf.write("\u00ff\3\2\2\2\u00ff\u00fd\3\2\2\2\u00ff\u0100\3\2\2\2")
        buf.write("\u0100\u0102\3\2\2\2\u0101\u0103\5K&\2\u0102\u0101\3\2")
        buf.write("\2\2\u0102\u0103\3\2\2\2\u0103\u0115\3\2\2\2\u0104\u0106")
        buf.write("\7\60\2\2\u0105\u0107\5\u008bF\2\u0106\u0105\3\2\2\2\u0107")
        buf.write("\u0108\3\2\2\2\u0108\u0106\3\2\2\2\u0108\u0109\3\2\2\2")
        buf.write("\u0109\u010b\3\2\2\2\u010a\u010c\5K&\2\u010b\u010a\3\2")
        buf.write("\2\2\u010b\u010c\3\2\2\2\u010c\u0115\3\2\2\2\u010d\u010f")
        buf.write("\5\u008bF\2\u010e\u010d\3\2\2\2\u010f\u0110\3\2\2\2\u0110")
        buf.write("\u010e\3\2\2\2\u0110\u0111\3\2\2\2\u0111\u0112\3\2\2\2")
        buf.write("\u0112\u0113\5K&\2\u0113\u0115\3\2\2\2\u0114\u00f7\3\2")
        buf.write("\2\2\u0114\u0104\3\2\2\2\u0114\u010e\3\2\2\2\u0115H\3")
        buf.write("\2\2\2\u0116\u0117\7v\2\2\u0117\u0118\7t\2\2\u0118\u0119")
        buf.write("\7w\2\2\u0119\u0120\7g\2\2\u011a\u011b\7h\2\2\u011b\u011c")
        buf.write("\7c\2\2\u011c\u011d\7n\2\2\u011d\u011e\7u\2\2\u011e\u0120")
        buf.write("\7g\2\2\u011f\u0116\3\2\2\2\u011f\u011a\3\2\2\2\u0120")
        buf.write("J\3\2\2\2\u0121\u0123\t\5\2\2\u0122\u0124\t\6\2\2\u0123")
        buf.write("\u0122\3\2\2\2\u0123\u0124\3\2\2\2\u0124\u0126\3\2\2\2")
        buf.write("\u0125\u0127\5\u008bF\2\u0126\u0125\3\2\2\2\u0127\u0128")
        buf.write("\3\2\2\2\u0128\u0126\3\2\2\2\u0128\u0129\3\2\2\2\u0129")
        buf.write("L\3\2\2\2\u012a\u012b\7e\2\2\u012b\u012c\7n\2\2\u012c")
        buf.write("\u012d\7c\2\2\u012d\u012e\7u\2\2\u012e\u012f\7u\2\2\u012f")
        buf.write("N\3\2\2\2\u0130\u0131\7c\2\2\u0131\u0132\7v\2\2\u0132")
        buf.write("\u0133\7v\2\2\u0133\u0134\7t\2\2\u0134P\3\2\2\2\u0135")
        buf.write("\u0136\7u\2\2\u0136\u0137\7v\2\2\u0137\u0138\7c\2\2\u0138")
        buf.write("\u0139\7v\2\2\u0139\u013a\7g\2\2\u013aR\3\2\2\2\u013b")
        buf.write("\u013c\7h\2\2\u013c\u013d\7w\2\2\u013d\u013e\7p\2\2\u013e")
        buf.write("\u013f\7e\2\2\u013fT\3\2\2\2\u0140\u0141\7r\2\2\u0141")
        buf.write("\u0142\7t\2\2\u0142\u0143\7g\2\2\u0143\u0144\7f\2\2\u0144")
        buf.write("V\3\2\2\2\u0145\u0146\7q\2\2\u0146\u0147\7r\2\2\u0147")
        buf.write("\u0148\7g\2\2\u0148\u0149\7t\2\2\u0149X\3\2\2\2\u014a")
        buf.write("\u014b\7k\2\2\u014b\u014c\7h\2\2\u014cZ\3\2\2\2\u014d")
        buf.write("\u014e\7g\2\2\u014e\u014f\7n\2\2\u014f\u0150\7u\2\2\u0150")
        buf.write("\u0151\7g\2\2\u0151\\\3\2\2\2\u0152\u0153\7g\2\2\u0153")
        buf.write("\u0154\7n\2\2\u0154\u0155\7k\2\2\u0155\u0156\7h\2\2\u0156")
        buf.write("^\3\2\2\2\u0157\u0158\7h\2\2\u0158\u0159\7q\2\2\u0159")
        buf.write("\u015a\7t\2\2\u015a`\3\2\2\2\u015b\u015c\7y\2\2\u015c")
        buf.write("\u015d\7j\2\2\u015d\u015e\7k\2\2\u015e\u015f\7n\2\2\u015f")
        buf.write("\u0160\7g\2\2\u0160b\3\2\2\2\u0161\u0162\7t\2\2\u0162")
        buf.write("\u0163\7g\2\2\u0163\u0164\7v\2\2\u0164d\3\2\2\2\u0165")
        buf.write("\u0166\7d\2\2\u0166\u0167\7t\2\2\u0167\u0168\7g\2\2\u0168")
        buf.write("\u0169\7c\2\2\u0169\u016a\7m\2\2\u016af\3\2\2\2\u016b")
        buf.write("\u016c\7e\2\2\u016c\u016d\7q\2\2\u016d\u016e\7p\2\2\u016e")
        buf.write("\u016f\7v\2\2\u016fh\3\2\2\2\u0170\u0171\7y\2\2\u0171")
        buf.write("\u0172\7j\2\2\u0172\u0173\7g\2\2\u0173\u0174\7p\2\2\u0174")
        buf.write("j\3\2\2\2\u0175\u0176\7g\2\2\u0176\u0177\7h\2\2\u0177")
        buf.write("\u0178\7h\2\2\u0178l\3\2\2\2\u0179\u017a\7g\2\2\u017a")
        buf.write("\u017b\7z\2\2\u017b\u017c\7g\2\2\u017c\u017d\7e\2\2\u017d")
        buf.write("n\3\2\2\2\u017e\u017f\7k\2\2\u017f\u0180\7p\2\2\u0180")
        buf.write("\u0181\7k\2\2\u0181\u0182\7v\2\2\u0182p\3\2\2\2\u0183")
        buf.write("\u0184\7i\2\2\u0184\u0185\7q\2\2\u0185\u0186\7c\2\2\u0186")
        buf.write("\u0187\7n\2\2\u0187r\3\2\2\2\u0188\u0189\7o\2\2\u0189")
        buf.write("\u018a\7c\2\2\u018a\u018b\7k\2\2\u018b\u018c\7p\2\2\u018c")
        buf.write("t\3\2\2\2\u018d\u018e\7k\2\2\u018e\u018f\7p\2\2\u018f")
        buf.write("v\3\2\2\2\u0190\u0191\7n\2\2\u0191\u0192\7k\2\2\u0192")
        buf.write("\u0193\7u\2\2\u0193\u0194\7v\2\2\u0194x\3\2\2\2\u0195")
        buf.write("\u0196\7d\2\2\u0196\u0197\7q\2\2\u0197\u0198\7q\2\2\u0198")
        buf.write("\u0199\7n\2\2\u0199z\3\2\2\2\u019a\u019b\7u\2\2\u019b")
        buf.write("\u019c\7v\2\2\u019c\u019d\7t\2\2\u019d|\3\2\2\2\u019e")
        buf.write("\u019f\7h\2\2\u019f\u01a0\7n\2\2\u01a0\u01a1\7q\2\2\u01a1")
        buf.write("\u01a2\7c\2\2\u01a2\u01a3\7v\2\2\u01a3~\3\2\2\2\u01a4")
        buf.write("\u01a5\7k\2\2\u01a5\u01a6\7p\2\2\u01a6\u01a7\7v\2\2\u01a7")
        buf.write("\u0080\3\2\2\2\u01a8\u01a9\7f\2\2\u01a9\u01aa\7q\2\2\u01aa")
        buf.write("\u01ab\7o\2\2\u01ab\u0082\3\2\2\2\u01ac\u01ad\7p\2\2\u01ad")
        buf.write("\u01ae\7w\2\2\u01ae\u01af\7o\2\2\u01af\u0084\3\2\2\2\u01b0")
        buf.write("\u01b1\7x\2\2\u01b1\u01b2\7c\2\2\u01b2\u01b3\7t\2\2\u01b3")
        buf.write("\u0086\3\2\2\2\u01b4\u01ba\5\u0089E\2\u01b5\u01b9\5\u0089")
        buf.write("E\2\u01b6\u01b9\7a\2\2\u01b7\u01b9\5\u008bF\2\u01b8\u01b5")
        buf.write("\3\2\2\2\u01b8\u01b6\3\2\2\2\u01b8\u01b7\3\2\2\2\u01b9")
        buf.write("\u01bc\3\2\2\2\u01ba\u01b8\3\2\2\2\u01ba\u01bb\3\2\2\2")
        buf.write("\u01bb\u0088\3\2\2\2\u01bc\u01ba\3\2\2\2\u01bd\u01be\t")
        buf.write("\7\2\2\u01be\u008a\3\2\2\2\u01bf\u01c0\t\b\2\2\u01c0\u008c")
        buf.write("\3\2\2\2\u01c1\u01c5\7%\2\2\u01c2\u01c4\n\t\2\2\u01c3")
        buf.write("\u01c2\3\2\2\2\u01c4\u01c7\3\2\2\2\u01c5\u01c3\3\2\2\2")
        buf.write("\u01c5\u01c6\3\2\2\2\u01c6\u01c8\3\2\2\2\u01c7\u01c5\3")
        buf.write("\2\2\2\u01c8\u01c9\bG\2\2\u01c9\u008e\3\2\2\2\u01ca\u01cc")
        buf.write("\t\n\2\2\u01cb\u01ca\3\2\2\2\u01cc\u01cd\3\2\2\2\u01cd")
        buf.write("\u01cb\3\2\2\2\u01cd\u01ce\3\2\2\2\u01ce\u01cf\3\2\2\2")
        buf.write("\u01cf\u01d0\bH\2\2\u01d0\u0090\3\2\2\2\27\2\u00dd\u00df")
        buf.write("\u00e6\u00e8\u00ec\u00f4\u00f9\u00ff\u0102\u0108\u010b")
        buf.write("\u0110\u0114\u011f\u0123\u0128\u01b8\u01ba\u01c5\u01cd")
        buf.write("\3\b\2\2")
        return buf.getvalue()


class EvansLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    T__14 = 15
    T__15 = 16
    T__16 = 17
    T__17 = 18
    T__18 = 19
    T__19 = 20
    T__20 = 21
    T__21 = 22
    T__22 = 23
    T__23 = 24
    T__24 = 25
    T__25 = 26
    T__26 = 27
    T__27 = 28
    T__28 = 29
    T__29 = 30
    T__30 = 31
    STRING_LITERAL = 32
    DECIMAL_LITERAL = 33
    FLOAT_LITERAL = 34
    BOOL_LITERAL = 35
    CLASS = 36
    ATTR = 37
    STATE = 38
    FUNC = 39
    PRED = 40
    OPER = 41
    IF = 42
    ELSE = 43
    ELIF = 44
    FOR = 45
    WHILE = 46
    RET = 47
    BREAK = 48
    CONT = 49
    WHEN = 50
    EFF = 51
    EXEC = 52
    INIT = 53
    GOAL = 54
    MAIN = 55
    IN = 56
    LIST = 57
    BOOL = 58
    STR = 59
    FLOAT = 60
    INT = 61
    DOM = 62
    NUM = 63
    VAR = 64
    ID = 65
    COMMENT = 66
    WS = 67

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'{'", "'}'", "':'", "'('", "')'", "','", "'='", "';'", "'.'", 
            "'+='", "'-='", "'*='", "'/='", "'%='", "'['", "']'", "'!'", 
            "'+'", "'-'", "'*'", "'/'", "'%'", "'<'", "'>'", "'<='", "'>='", 
            "'!='", "'=='", "'&&'", "'||'", "'?'", "'class'", "'attr'", 
            "'state'", "'func'", "'pred'", "'oper'", "'if'", "'else'", "'elif'", 
            "'for'", "'while'", "'ret'", "'break'", "'cont'", "'when'", 
            "'eff'", "'exec'", "'init'", "'goal'", "'main'", "'in'", "'list'", 
            "'bool'", "'str'", "'float'", "'int'", "'dom'", "'num'", "'var'" ]

    symbolicNames = [ "<INVALID>",
            "STRING_LITERAL", "DECIMAL_LITERAL", "FLOAT_LITERAL", "BOOL_LITERAL", 
            "CLASS", "ATTR", "STATE", "FUNC", "PRED", "OPER", "IF", "ELSE", 
            "ELIF", "FOR", "WHILE", "RET", "BREAK", "CONT", "WHEN", "EFF", 
            "EXEC", "INIT", "GOAL", "MAIN", "IN", "LIST", "BOOL", "STR", 
            "FLOAT", "INT", "DOM", "NUM", "VAR", "ID", "COMMENT", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "T__17", "T__18", "T__19", 
                  "T__20", "T__21", "T__22", "T__23", "T__24", "T__25", 
                  "T__26", "T__27", "T__28", "T__29", "T__30", "STRING_LITERAL", 
                  "STRING_ESCAPE", "DECIMAL_LITERAL", "FLOAT_LITERAL", "BOOL_LITERAL", 
                  "EXPONENT", "CLASS", "ATTR", "STATE", "FUNC", "PRED", 
                  "OPER", "IF", "ELSE", "ELIF", "FOR", "WHILE", "RET", "BREAK", 
                  "CONT", "WHEN", "EFF", "EXEC", "INIT", "GOAL", "MAIN", 
                  "IN", "LIST", "BOOL", "STR", "FLOAT", "INT", "DOM", "NUM", 
                  "VAR", "ID", "LETTER", "DIGIT", "COMMENT", "WS" ]

    grammarFileName = "Evans.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


