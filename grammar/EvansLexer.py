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
        buf.write("\3\17\3\17\3\20\3\20\3\21\3\21\3\22\3\22\3\23\3\23\3\23")
        buf.write("\3\24\3\24\3\24\3\25\3\25\3\26\3\26\3\26\7\26\u00c4\n")
        buf.write("\26\f\26\16\26\u00c7\13\26\3\26\3\26\3\26\3\26\7\26\u00cd")
        buf.write("\n\26\f\26\16\26\u00d0\13\26\3\26\5\26\u00d3\n\26\3\27")
        buf.write("\3\27\3\27\3\30\6\30\u00d9\n\30\r\30\16\30\u00da\3\31")
        buf.write("\6\31\u00de\n\31\r\31\16\31\u00df\3\31\3\31\6\31\u00e4")
        buf.write("\n\31\r\31\16\31\u00e5\3\31\5\31\u00e9\n\31\3\31\3\31")
        buf.write("\6\31\u00ed\n\31\r\31\16\31\u00ee\3\31\5\31\u00f2\n\31")
        buf.write("\3\31\6\31\u00f5\n\31\r\31\16\31\u00f6\3\31\3\31\5\31")
        buf.write("\u00fb\n\31\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3")
        buf.write("\32\5\32\u0106\n\32\3\33\3\33\5\33\u010a\n\33\3\33\6\33")
        buf.write("\u010d\n\33\r\33\16\33\u010e\3\34\3\34\3\34\3\34\3\34")
        buf.write("\3\34\3\35\3\35\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\36\3\37\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3 \3!\3!\3")
        buf.write("!\3!\3!\3\"\3\"\3\"\3#\3#\3#\3#\3#\3$\3$\3$\3$\3$\3%\3")
        buf.write("%\3%\3%\3&\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3(\3(\3(\3(")
        buf.write("\3(\3(\3)\3)\3)\3)\3)\3*\3*\3*\3*\3*\3+\3+\3+\3+\3,\3")
        buf.write(",\3,\3,\3,\3-\3-\3-\3-\3-\3.\3.\3.\3.\3.\3/\3/\3/\3/\3")
        buf.write("/\3\60\3\60\3\60\3\61\3\61\3\61\3\61\3\62\3\62\3\62\3")
        buf.write("\62\3\62\3\63\3\63\3\63\3\63\3\63\3\64\3\64\3\64\3\64")
        buf.write("\3\65\3\65\3\65\3\65\3\65\3\65\3\66\3\66\3\66\3\66\3\67")
        buf.write("\3\67\3\67\3\67\38\38\38\38\39\39\3:\3:\3;\3;\3<\3<\3")
        buf.write("=\3=\3>\3>\3?\3?\3@\3@\3@\3A\3A\3A\3B\3B\3B\3C\3C\3C\3")
        buf.write("D\3D\3D\3D\7D\u01b9\nD\fD\16D\u01bc\13D\3E\3E\3F\3F\3")
        buf.write("G\3G\7G\u01c4\nG\fG\16G\u01c7\13G\3G\3G\3H\6H\u01cc\n")
        buf.write("H\rH\16H\u01cd\3H\3H\2\2I\3\3\5\4\7\5\t\6\13\7\r\b\17")
        buf.write("\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23")
        buf.write("%\24\'\25)\26+\27-\2/\30\61\31\63\32\65\2\67\339\34;\35")
        buf.write("=\36?\37A C!E\"G#I$K%M&O\'Q(S)U*W+Y,[-]._/a\60c\61e\62")
        buf.write("g\63i\64k\65m\66o\67q8s9u:w;y<{=}>\177?\u0081@\u0083A")
        buf.write("\u0085B\u0087C\u0089\2\u008b\2\u008dD\u008fE\3\2\13\4")
        buf.write("\2$$^^\4\2))^^\n\2$$))^^ddhhppttvv\4\2GGgg\4\2--//\4\2")
        buf.write("C\\c|\3\2\62;\4\2\f\f\16\17\5\2\13\f\17\17\"\"\2\u01e2")
        buf.write("\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13")
        buf.write("\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3")
        buf.write("\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2")
        buf.write("\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2")
        buf.write("%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2/\3\2\2\2")
        buf.write("\2\61\3\2\2\2\2\63\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;")
        buf.write("\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2")
        buf.write("E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2")
        buf.write("\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2")
        buf.write("\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2")
        buf.write("\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3")
        buf.write("\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2s\3\2\2\2\2u")
        buf.write("\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2")
        buf.write("\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2\2\2\u0085\3")
        buf.write("\2\2\2\2\u0087\3\2\2\2\2\u008d\3\2\2\2\2\u008f\3\2\2\2")
        buf.write("\3\u0091\3\2\2\2\5\u0093\3\2\2\2\7\u0095\3\2\2\2\t\u0097")
        buf.write("\3\2\2\2\13\u0099\3\2\2\2\r\u009b\3\2\2\2\17\u009d\3\2")
        buf.write("\2\2\21\u009f\3\2\2\2\23\u00a1\3\2\2\2\25\u00a3\3\2\2")
        buf.write("\2\27\u00a6\3\2\2\2\31\u00a9\3\2\2\2\33\u00ac\3\2\2\2")
        buf.write("\35\u00af\3\2\2\2\37\u00b2\3\2\2\2!\u00b4\3\2\2\2#\u00b6")
        buf.write("\3\2\2\2%\u00b8\3\2\2\2\'\u00bb\3\2\2\2)\u00be\3\2\2\2")
        buf.write("+\u00d2\3\2\2\2-\u00d4\3\2\2\2/\u00d8\3\2\2\2\61\u00fa")
        buf.write("\3\2\2\2\63\u0105\3\2\2\2\65\u0107\3\2\2\2\67\u0110\3")
        buf.write("\2\2\29\u0116\3\2\2\2;\u011b\3\2\2\2=\u0121\3\2\2\2?\u0126")
        buf.write("\3\2\2\2A\u012b\3\2\2\2C\u0130\3\2\2\2E\u0133\3\2\2\2")
        buf.write("G\u0138\3\2\2\2I\u013d\3\2\2\2K\u0141\3\2\2\2M\u0147\3")
        buf.write("\2\2\2O\u014b\3\2\2\2Q\u0151\3\2\2\2S\u0156\3\2\2\2U\u015b")
        buf.write("\3\2\2\2W\u015f\3\2\2\2Y\u0164\3\2\2\2[\u0169\3\2\2\2")
        buf.write("]\u016e\3\2\2\2_\u0173\3\2\2\2a\u0176\3\2\2\2c\u017a\3")
        buf.write("\2\2\2e\u017f\3\2\2\2g\u0184\3\2\2\2i\u0188\3\2\2\2k\u018e")
        buf.write("\3\2\2\2m\u0192\3\2\2\2o\u0196\3\2\2\2q\u019a\3\2\2\2")
        buf.write("s\u019c\3\2\2\2u\u019e\3\2\2\2w\u01a0\3\2\2\2y\u01a2\3")
        buf.write("\2\2\2{\u01a4\3\2\2\2}\u01a6\3\2\2\2\177\u01a8\3\2\2\2")
        buf.write("\u0081\u01ab\3\2\2\2\u0083\u01ae\3\2\2\2\u0085\u01b1\3")
        buf.write("\2\2\2\u0087\u01b4\3\2\2\2\u0089\u01bd\3\2\2\2\u008b\u01bf")
        buf.write("\3\2\2\2\u008d\u01c1\3\2\2\2\u008f\u01cb\3\2\2\2\u0091")
        buf.write("\u0092\7}\2\2\u0092\4\3\2\2\2\u0093\u0094\7\177\2\2\u0094")
        buf.write("\6\3\2\2\2\u0095\u0096\7<\2\2\u0096\b\3\2\2\2\u0097\u0098")
        buf.write("\7*\2\2\u0098\n\3\2\2\2\u0099\u009a\7+\2\2\u009a\f\3\2")
        buf.write("\2\2\u009b\u009c\7.\2\2\u009c\16\3\2\2\2\u009d\u009e\7")
        buf.write("?\2\2\u009e\20\3\2\2\2\u009f\u00a0\7=\2\2\u00a0\22\3\2")
        buf.write("\2\2\u00a1\u00a2\7\60\2\2\u00a2\24\3\2\2\2\u00a3\u00a4")
        buf.write("\7-\2\2\u00a4\u00a5\7?\2\2\u00a5\26\3\2\2\2\u00a6\u00a7")
        buf.write("\7/\2\2\u00a7\u00a8\7?\2\2\u00a8\30\3\2\2\2\u00a9\u00aa")
        buf.write("\7,\2\2\u00aa\u00ab\7?\2\2\u00ab\32\3\2\2\2\u00ac\u00ad")
        buf.write("\7\61\2\2\u00ad\u00ae\7?\2\2\u00ae\34\3\2\2\2\u00af\u00b0")
        buf.write("\7\'\2\2\u00b0\u00b1\7?\2\2\u00b1\36\3\2\2\2\u00b2\u00b3")
        buf.write("\7]\2\2\u00b3 \3\2\2\2\u00b4\u00b5\7_\2\2\u00b5\"\3\2")
        buf.write("\2\2\u00b6\u00b7\7#\2\2\u00b7$\3\2\2\2\u00b8\u00b9\7(")
        buf.write("\2\2\u00b9\u00ba\7(\2\2\u00ba&\3\2\2\2\u00bb\u00bc\7~")
        buf.write("\2\2\u00bc\u00bd\7~\2\2\u00bd(\3\2\2\2\u00be\u00bf\7A")
        buf.write("\2\2\u00bf*\3\2\2\2\u00c0\u00c5\7$\2\2\u00c1\u00c4\5-")
        buf.write("\27\2\u00c2\u00c4\n\2\2\2\u00c3\u00c1\3\2\2\2\u00c3\u00c2")
        buf.write("\3\2\2\2\u00c4\u00c7\3\2\2\2\u00c5\u00c3\3\2\2\2\u00c5")
        buf.write("\u00c6\3\2\2\2\u00c6\u00c8\3\2\2\2\u00c7\u00c5\3\2\2\2")
        buf.write("\u00c8\u00d3\7$\2\2\u00c9\u00ce\7)\2\2\u00ca\u00cd\5-")
        buf.write("\27\2\u00cb\u00cd\n\3\2\2\u00cc\u00ca\3\2\2\2\u00cc\u00cb")
        buf.write("\3\2\2\2\u00cd\u00d0\3\2\2\2\u00ce\u00cc\3\2\2\2\u00ce")
        buf.write("\u00cf\3\2\2\2\u00cf\u00d1\3\2\2\2\u00d0\u00ce\3\2\2\2")
        buf.write("\u00d1\u00d3\7)\2\2\u00d2\u00c0\3\2\2\2\u00d2\u00c9\3")
        buf.write("\2\2\2\u00d3,\3\2\2\2\u00d4\u00d5\7^\2\2\u00d5\u00d6\t")
        buf.write("\4\2\2\u00d6.\3\2\2\2\u00d7\u00d9\5\u008bF\2\u00d8\u00d7")
        buf.write("\3\2\2\2\u00d9\u00da\3\2\2\2\u00da\u00d8\3\2\2\2\u00da")
        buf.write("\u00db\3\2\2\2\u00db\60\3\2\2\2\u00dc\u00de\5\u008bF\2")
        buf.write("\u00dd\u00dc\3\2\2\2\u00de\u00df\3\2\2\2\u00df\u00dd\3")
        buf.write("\2\2\2\u00df\u00e0\3\2\2\2\u00e0\u00e1\3\2\2\2\u00e1\u00e3")
        buf.write("\7\60\2\2\u00e2\u00e4\5\u008bF\2\u00e3\u00e2\3\2\2\2\u00e4")
        buf.write("\u00e5\3\2\2\2\u00e5\u00e3\3\2\2\2\u00e5\u00e6\3\2\2\2")
        buf.write("\u00e6\u00e8\3\2\2\2\u00e7\u00e9\5\65\33\2\u00e8\u00e7")
        buf.write("\3\2\2\2\u00e8\u00e9\3\2\2\2\u00e9\u00fb\3\2\2\2\u00ea")
        buf.write("\u00ec\7\60\2\2\u00eb\u00ed\5\u008bF\2\u00ec\u00eb\3\2")
        buf.write("\2\2\u00ed\u00ee\3\2\2\2\u00ee\u00ec\3\2\2\2\u00ee\u00ef")
        buf.write("\3\2\2\2\u00ef\u00f1\3\2\2\2\u00f0\u00f2\5\65\33\2\u00f1")
        buf.write("\u00f0\3\2\2\2\u00f1\u00f2\3\2\2\2\u00f2\u00fb\3\2\2\2")
        buf.write("\u00f3\u00f5\5\u008bF\2\u00f4\u00f3\3\2\2\2\u00f5\u00f6")
        buf.write("\3\2\2\2\u00f6\u00f4\3\2\2\2\u00f6\u00f7\3\2\2\2\u00f7")
        buf.write("\u00f8\3\2\2\2\u00f8\u00f9\5\65\33\2\u00f9\u00fb\3\2\2")
        buf.write("\2\u00fa\u00dd\3\2\2\2\u00fa\u00ea\3\2\2\2\u00fa\u00f4")
        buf.write("\3\2\2\2\u00fb\62\3\2\2\2\u00fc\u00fd\7v\2\2\u00fd\u00fe")
        buf.write("\7t\2\2\u00fe\u00ff\7w\2\2\u00ff\u0106\7g\2\2\u0100\u0101")
        buf.write("\7h\2\2\u0101\u0102\7c\2\2\u0102\u0103\7n\2\2\u0103\u0104")
        buf.write("\7u\2\2\u0104\u0106\7g\2\2\u0105\u00fc\3\2\2\2\u0105\u0100")
        buf.write("\3\2\2\2\u0106\64\3\2\2\2\u0107\u0109\t\5\2\2\u0108\u010a")
        buf.write("\t\6\2\2\u0109\u0108\3\2\2\2\u0109\u010a\3\2\2\2\u010a")
        buf.write("\u010c\3\2\2\2\u010b\u010d\5\u008bF\2\u010c\u010b\3\2")
        buf.write("\2\2\u010d\u010e\3\2\2\2\u010e\u010c\3\2\2\2\u010e\u010f")
        buf.write("\3\2\2\2\u010f\66\3\2\2\2\u0110\u0111\7e\2\2\u0111\u0112")
        buf.write("\7n\2\2\u0112\u0113\7c\2\2\u0113\u0114\7u\2\2\u0114\u0115")
        buf.write("\7u\2\2\u01158\3\2\2\2\u0116\u0117\7c\2\2\u0117\u0118")
        buf.write("\7v\2\2\u0118\u0119\7v\2\2\u0119\u011a\7t\2\2\u011a:\3")
        buf.write("\2\2\2\u011b\u011c\7u\2\2\u011c\u011d\7v\2\2\u011d\u011e")
        buf.write("\7c\2\2\u011e\u011f\7v\2\2\u011f\u0120\7g\2\2\u0120<\3")
        buf.write("\2\2\2\u0121\u0122\7h\2\2\u0122\u0123\7w\2\2\u0123\u0124")
        buf.write("\7p\2\2\u0124\u0125\7e\2\2\u0125>\3\2\2\2\u0126\u0127")
        buf.write("\7r\2\2\u0127\u0128\7t\2\2\u0128\u0129\7g\2\2\u0129\u012a")
        buf.write("\7f\2\2\u012a@\3\2\2\2\u012b\u012c\7q\2\2\u012c\u012d")
        buf.write("\7r\2\2\u012d\u012e\7g\2\2\u012e\u012f\7t\2\2\u012fB\3")
        buf.write("\2\2\2\u0130\u0131\7k\2\2\u0131\u0132\7h\2\2\u0132D\3")
        buf.write("\2\2\2\u0133\u0134\7g\2\2\u0134\u0135\7n\2\2\u0135\u0136")
        buf.write("\7k\2\2\u0136\u0137\7h\2\2\u0137F\3\2\2\2\u0138\u0139")
        buf.write("\7g\2\2\u0139\u013a\7n\2\2\u013a\u013b\7u\2\2\u013b\u013c")
        buf.write("\7g\2\2\u013cH\3\2\2\2\u013d\u013e\7h\2\2\u013e\u013f")
        buf.write("\7q\2\2\u013f\u0140\7t\2\2\u0140J\3\2\2\2\u0141\u0142")
        buf.write("\7y\2\2\u0142\u0143\7j\2\2\u0143\u0144\7k\2\2\u0144\u0145")
        buf.write("\7n\2\2\u0145\u0146\7g\2\2\u0146L\3\2\2\2\u0147\u0148")
        buf.write("\7t\2\2\u0148\u0149\7g\2\2\u0149\u014a\7v\2\2\u014aN\3")
        buf.write("\2\2\2\u014b\u014c\7d\2\2\u014c\u014d\7t\2\2\u014d\u014e")
        buf.write("\7g\2\2\u014e\u014f\7c\2\2\u014f\u0150\7m\2\2\u0150P\3")
        buf.write("\2\2\2\u0151\u0152\7e\2\2\u0152\u0153\7q\2\2\u0153\u0154")
        buf.write("\7p\2\2\u0154\u0155\7v\2\2\u0155R\3\2\2\2\u0156\u0157")
        buf.write("\7y\2\2\u0157\u0158\7j\2\2\u0158\u0159\7g\2\2\u0159\u015a")
        buf.write("\7p\2\2\u015aT\3\2\2\2\u015b\u015c\7g\2\2\u015c\u015d")
        buf.write("\7h\2\2\u015d\u015e\7h\2\2\u015eV\3\2\2\2\u015f\u0160")
        buf.write("\7g\2\2\u0160\u0161\7z\2\2\u0161\u0162\7g\2\2\u0162\u0163")
        buf.write("\7e\2\2\u0163X\3\2\2\2\u0164\u0165\7k\2\2\u0165\u0166")
        buf.write("\7p\2\2\u0166\u0167\7k\2\2\u0167\u0168\7v\2\2\u0168Z\3")
        buf.write("\2\2\2\u0169\u016a\7i\2\2\u016a\u016b\7q\2\2\u016b\u016c")
        buf.write("\7c\2\2\u016c\u016d\7n\2\2\u016d\\\3\2\2\2\u016e\u016f")
        buf.write("\7o\2\2\u016f\u0170\7c\2\2\u0170\u0171\7k\2\2\u0171\u0172")
        buf.write("\7p\2\2\u0172^\3\2\2\2\u0173\u0174\7k\2\2\u0174\u0175")
        buf.write("\7p\2\2\u0175`\3\2\2\2\u0176\u0177\7f\2\2\u0177\u0178")
        buf.write("\7q\2\2\u0178\u0179\7o\2\2\u0179b\3\2\2\2\u017a\u017b")
        buf.write("\7n\2\2\u017b\u017c\7k\2\2\u017c\u017d\7u\2\2\u017d\u017e")
        buf.write("\7v\2\2\u017ed\3\2\2\2\u017f\u0180\7d\2\2\u0180\u0181")
        buf.write("\7q\2\2\u0181\u0182\7q\2\2\u0182\u0183\7n\2\2\u0183f\3")
        buf.write("\2\2\2\u0184\u0185\7u\2\2\u0185\u0186\7v\2\2\u0186\u0187")
        buf.write("\7t\2\2\u0187h\3\2\2\2\u0188\u0189\7h\2\2\u0189\u018a")
        buf.write("\7n\2\2\u018a\u018b\7q\2\2\u018b\u018c\7c\2\2\u018c\u018d")
        buf.write("\7v\2\2\u018dj\3\2\2\2\u018e\u018f\7k\2\2\u018f\u0190")
        buf.write("\7p\2\2\u0190\u0191\7v\2\2\u0191l\3\2\2\2\u0192\u0193")
        buf.write("\7p\2\2\u0193\u0194\7w\2\2\u0194\u0195\7o\2\2\u0195n\3")
        buf.write("\2\2\2\u0196\u0197\7x\2\2\u0197\u0198\7c\2\2\u0198\u0199")
        buf.write("\7t\2\2\u0199p\3\2\2\2\u019a\u019b\7,\2\2\u019br\3\2\2")
        buf.write("\2\u019c\u019d\7\61\2\2\u019dt\3\2\2\2\u019e\u019f\7\'")
        buf.write("\2\2\u019fv\3\2\2\2\u01a0\u01a1\7-\2\2\u01a1x\3\2\2\2")
        buf.write("\u01a2\u01a3\7/\2\2\u01a3z\3\2\2\2\u01a4\u01a5\7>\2\2")
        buf.write("\u01a5|\3\2\2\2\u01a6\u01a7\7@\2\2\u01a7~\3\2\2\2\u01a8")
        buf.write("\u01a9\7>\2\2\u01a9\u01aa\7?\2\2\u01aa\u0080\3\2\2\2\u01ab")
        buf.write("\u01ac\7@\2\2\u01ac\u01ad\7?\2\2\u01ad\u0082\3\2\2\2\u01ae")
        buf.write("\u01af\7#\2\2\u01af\u01b0\7?\2\2\u01b0\u0084\3\2\2\2\u01b1")
        buf.write("\u01b2\7?\2\2\u01b2\u01b3\7?\2\2\u01b3\u0086\3\2\2\2\u01b4")
        buf.write("\u01ba\5\u0089E\2\u01b5\u01b9\5\u0089E\2\u01b6\u01b9\7")
        buf.write("a\2\2\u01b7\u01b9\5\u008bF\2\u01b8\u01b5\3\2\2\2\u01b8")
        buf.write("\u01b6\3\2\2\2\u01b8\u01b7\3\2\2\2\u01b9\u01bc\3\2\2\2")
        buf.write("\u01ba\u01b8\3\2\2\2\u01ba\u01bb\3\2\2\2\u01bb\u0088\3")
        buf.write("\2\2\2\u01bc\u01ba\3\2\2\2\u01bd\u01be\t\7\2\2\u01be\u008a")
        buf.write("\3\2\2\2\u01bf\u01c0\t\b\2\2\u01c0\u008c\3\2\2\2\u01c1")
        buf.write("\u01c5\7%\2\2\u01c2\u01c4\n\t\2\2\u01c3\u01c2\3\2\2\2")
        buf.write("\u01c4\u01c7\3\2\2\2\u01c5\u01c3\3\2\2\2\u01c5\u01c6\3")
        buf.write("\2\2\2\u01c6\u01c8\3\2\2\2\u01c7\u01c5\3\2\2\2\u01c8\u01c9")
        buf.write("\bG\2\2\u01c9\u008e\3\2\2\2\u01ca\u01cc\t\n\2\2\u01cb")
        buf.write("\u01ca\3\2\2\2\u01cc\u01cd\3\2\2\2\u01cd\u01cb\3\2\2\2")
        buf.write("\u01cd\u01ce\3\2\2\2\u01ce\u01cf\3\2\2\2\u01cf\u01d0\b")
        buf.write("H\2\2\u01d0\u0090\3\2\2\2\27\2\u00c3\u00c5\u00cc\u00ce")
        buf.write("\u00d2\u00da\u00df\u00e5\u00e8\u00ee\u00f1\u00f6\u00fa")
        buf.write("\u0105\u0109\u010e\u01b8\u01ba\u01c5\u01cd\3\b\2\2")
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
    STRING_LITERAL = 21
    DECIMAL_LITERAL = 22
    FLOAT_LITERAL = 23
    BOOL_LITERAL = 24
    CLASS = 25
    ATTR = 26
    STATE = 27
    FUNC = 28
    PRED = 29
    OPER = 30
    IF = 31
    ELIF = 32
    ELSE = 33
    FOR = 34
    WHILE = 35
    RET = 36
    BREAK = 37
    CONT = 38
    WHEN = 39
    EFF = 40
    EXEC = 41
    INIT = 42
    GOAL = 43
    MAIN = 44
    IN = 45
    DOM = 46
    LIST = 47
    BOOL = 48
    STR = 49
    FLOAT = 50
    INT = 51
    NUM = 52
    VAR = 53
    MUL = 54
    DIV = 55
    MOD = 56
    ADD = 57
    SUB = 58
    LT = 59
    GT = 60
    LE = 61
    GE = 62
    NE = 63
    EQ = 64
    ID = 65
    COMMENT = 66
    WS = 67

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'{'", "'}'", "':'", "'('", "')'", "','", "'='", "';'", "'.'", 
            "'+='", "'-='", "'*='", "'/='", "'%='", "'['", "']'", "'!'", 
            "'&&'", "'||'", "'?'", "'class'", "'attr'", "'state'", "'func'", 
            "'pred'", "'oper'", "'if'", "'elif'", "'else'", "'for'", "'while'", 
            "'ret'", "'break'", "'cont'", "'when'", "'eff'", "'exec'", "'init'", 
            "'goal'", "'main'", "'in'", "'dom'", "'list'", "'bool'", "'str'", 
            "'float'", "'int'", "'num'", "'var'", "'*'", "'/'", "'%'", "'+'", 
            "'-'", "'<'", "'>'", "'<='", "'>='", "'!='", "'=='" ]

    symbolicNames = [ "<INVALID>",
            "STRING_LITERAL", "DECIMAL_LITERAL", "FLOAT_LITERAL", "BOOL_LITERAL", 
            "CLASS", "ATTR", "STATE", "FUNC", "PRED", "OPER", "IF", "ELIF", 
            "ELSE", "FOR", "WHILE", "RET", "BREAK", "CONT", "WHEN", "EFF", 
            "EXEC", "INIT", "GOAL", "MAIN", "IN", "DOM", "LIST", "BOOL", 
            "STR", "FLOAT", "INT", "NUM", "VAR", "MUL", "DIV", "MOD", "ADD", 
            "SUB", "LT", "GT", "LE", "GE", "NE", "EQ", "ID", "COMMENT", 
            "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "T__17", "T__18", "T__19", 
                  "STRING_LITERAL", "STRING_ESCAPE", "DECIMAL_LITERAL", 
                  "FLOAT_LITERAL", "BOOL_LITERAL", "EXPONENT", "CLASS", 
                  "ATTR", "STATE", "FUNC", "PRED", "OPER", "IF", "ELIF", 
                  "ELSE", "FOR", "WHILE", "RET", "BREAK", "CONT", "WHEN", 
                  "EFF", "EXEC", "INIT", "GOAL", "MAIN", "IN", "DOM", "LIST", 
                  "BOOL", "STR", "FLOAT", "INT", "NUM", "VAR", "MUL", "DIV", 
                  "MOD", "ADD", "SUB", "LT", "GT", "LE", "GE", "NE", "EQ", 
                  "ID", "LETTER", "DIGIT", "COMMENT", "WS" ]

    grammarFileName = "Evans.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


