# Generated from grammar/Evans.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2G")
        buf.write("\u01df\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\3\2\3\2\3")
        buf.write("\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t")
        buf.write("\3\n\3\n\3\13\3\13\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3\16")
        buf.write("\3\17\3\17\3\17\3\20\3\20\3\20\3\21\3\21\3\21\3\22\3\22")
        buf.write("\3\23\3\23\3\23\3\24\3\24\3\24\3\25\3\25\3\26\3\26\3\26")
        buf.write("\7\26\u00c8\n\26\f\26\16\26\u00cb\13\26\3\26\3\26\3\26")
        buf.write("\3\26\7\26\u00d1\n\26\f\26\16\26\u00d4\13\26\3\26\5\26")
        buf.write("\u00d7\n\26\3\27\3\27\3\27\3\30\6\30\u00dd\n\30\r\30\16")
        buf.write("\30\u00de\3\31\6\31\u00e2\n\31\r\31\16\31\u00e3\3\31\3")
        buf.write("\31\6\31\u00e8\n\31\r\31\16\31\u00e9\3\31\5\31\u00ed\n")
        buf.write("\31\3\31\3\31\6\31\u00f1\n\31\r\31\16\31\u00f2\3\31\5")
        buf.write("\31\u00f6\n\31\3\31\6\31\u00f9\n\31\r\31\16\31\u00fa\3")
        buf.write("\31\3\31\5\31\u00ff\n\31\3\32\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\32\5\32\u010a\n\32\3\33\3\33\5\33\u010e\n")
        buf.write("\33\3\33\6\33\u0111\n\33\r\33\16\33\u0112\3\34\3\34\3")
        buf.write("\34\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\35\3\36\3\36")
        buf.write("\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3\37\3 \3 \3")
        buf.write(" \3 \3 \3!\3!\3!\3!\3!\3\"\3\"\3\"\3#\3#\3#\3#\3#\3$\3")
        buf.write("$\3$\3$\3$\3%\3%\3%\3%\3&\3&\3&\3&\3&\3&\3\'\3\'\3\'\3")
        buf.write("\'\3(\3(\3(\3(\3(\3(\3)\3)\3)\3)\3)\3*\3*\3*\3*\3*\3+")
        buf.write("\3+\3+\3+\3,\3,\3,\3,\3,\3-\3-\3-\3-\3-\3.\3.\3.\3.\3")
        buf.write(".\3/\3/\3/\3/\3/\3\60\3\60\3\60\3\61\3\61\3\61\3\61\3")
        buf.write("\62\3\62\3\62\3\62\3\63\3\63\3\63\3\63\3\63\3\63\3\64")
        buf.write("\3\64\3\64\3\64\3\64\3\65\3\65\3\65\3\65\3\65\3\66\3\66")
        buf.write("\3\66\3\66\3\67\3\67\3\67\3\67\3\67\3\67\38\38\38\38\3")
        buf.write("9\39\39\39\3:\3:\3:\3:\3;\3;\3<\3<\3=\3=\3>\3>\3?\3?\3")
        buf.write("@\3@\3A\3A\3B\3B\3B\3C\3C\3C\3D\3D\3D\3E\3E\3E\3F\3F\3")
        buf.write("F\3F\7F\u01c7\nF\fF\16F\u01ca\13F\3G\3G\3H\3H\3I\3I\7")
        buf.write("I\u01d2\nI\fI\16I\u01d5\13I\3I\3I\3J\6J\u01da\nJ\rJ\16")
        buf.write("J\u01db\3J\3J\2\2K\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n")
        buf.write("\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'")
        buf.write("\25)\26+\27-\2/\30\61\31\63\32\65\2\67\339\34;\35=\36")
        buf.write("?\37A C!E\"G#I$K%M&O\'Q(S)U*W+Y,[-]._/a\60c\61e\62g\63")
        buf.write("i\64k\65m\66o\67q8s9u:w;y<{=}>\177?\u0081@\u0083A\u0085")
        buf.write("B\u0087C\u0089D\u008bE\u008d\2\u008f\2\u0091F\u0093G\3")
        buf.write("\2\13\4\2$$^^\4\2))^^\n\2$$))^^ddhhppttvv\4\2GGgg\4\2")
        buf.write("--//\4\2C\\c|\3\2\62;\4\2\f\f\16\17\5\2\13\f\17\17\"\"")
        buf.write("\2\u01f0\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2")
        buf.write("\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2")
        buf.write("\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2")
        buf.write("\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3")
        buf.write("\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2")
        buf.write("/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\67\3\2\2\2\29\3")
        buf.write("\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C")
        buf.write("\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2")
        buf.write("M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2")
        buf.write("\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2")
        buf.write("\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2")
        buf.write("\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2s\3")
        buf.write("\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}")
        buf.write("\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2\2")
        buf.write("\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2\2\2\2\u008b")
        buf.write("\3\2\2\2\2\u0091\3\2\2\2\2\u0093\3\2\2\2\3\u0095\3\2\2")
        buf.write("\2\5\u0097\3\2\2\2\7\u0099\3\2\2\2\t\u009b\3\2\2\2\13")
        buf.write("\u009d\3\2\2\2\r\u009f\3\2\2\2\17\u00a1\3\2\2\2\21\u00a3")
        buf.write("\3\2\2\2\23\u00a5\3\2\2\2\25\u00a7\3\2\2\2\27\u00a9\3")
        buf.write("\2\2\2\31\u00ab\3\2\2\2\33\u00ae\3\2\2\2\35\u00b1\3\2")
        buf.write("\2\2\37\u00b4\3\2\2\2!\u00b7\3\2\2\2#\u00ba\3\2\2\2%\u00bc")
        buf.write("\3\2\2\2\'\u00bf\3\2\2\2)\u00c2\3\2\2\2+\u00d6\3\2\2\2")
        buf.write("-\u00d8\3\2\2\2/\u00dc\3\2\2\2\61\u00fe\3\2\2\2\63\u0109")
        buf.write("\3\2\2\2\65\u010b\3\2\2\2\67\u0114\3\2\2\29\u011a\3\2")
        buf.write("\2\2;\u011f\3\2\2\2=\u0125\3\2\2\2?\u012a\3\2\2\2A\u012f")
        buf.write("\3\2\2\2C\u0134\3\2\2\2E\u0137\3\2\2\2G\u013c\3\2\2\2")
        buf.write("I\u0141\3\2\2\2K\u0145\3\2\2\2M\u014b\3\2\2\2O\u014f\3")
        buf.write("\2\2\2Q\u0155\3\2\2\2S\u015a\3\2\2\2U\u015f\3\2\2\2W\u0163")
        buf.write("\3\2\2\2Y\u0168\3\2\2\2[\u016d\3\2\2\2]\u0172\3\2\2\2")
        buf.write("_\u0177\3\2\2\2a\u017a\3\2\2\2c\u017e\3\2\2\2e\u0182\3")
        buf.write("\2\2\2g\u0188\3\2\2\2i\u018d\3\2\2\2k\u0192\3\2\2\2m\u0196")
        buf.write("\3\2\2\2o\u019c\3\2\2\2q\u01a0\3\2\2\2s\u01a4\3\2\2\2")
        buf.write("u\u01a8\3\2\2\2w\u01aa\3\2\2\2y\u01ac\3\2\2\2{\u01ae\3")
        buf.write("\2\2\2}\u01b0\3\2\2\2\177\u01b2\3\2\2\2\u0081\u01b4\3")
        buf.write("\2\2\2\u0083\u01b6\3\2\2\2\u0085\u01b9\3\2\2\2\u0087\u01bc")
        buf.write("\3\2\2\2\u0089\u01bf\3\2\2\2\u008b\u01c2\3\2\2\2\u008d")
        buf.write("\u01cb\3\2\2\2\u008f\u01cd\3\2\2\2\u0091\u01cf\3\2\2\2")
        buf.write("\u0093\u01d9\3\2\2\2\u0095\u0096\7}\2\2\u0096\4\3\2\2")
        buf.write("\2\u0097\u0098\7\177\2\2\u0098\6\3\2\2\2\u0099\u009a\7")
        buf.write("<\2\2\u009a\b\3\2\2\2\u009b\u009c\7*\2\2\u009c\n\3\2\2")
        buf.write("\2\u009d\u009e\7+\2\2\u009e\f\3\2\2\2\u009f\u00a0\7.\2")
        buf.write("\2\u00a0\16\3\2\2\2\u00a1\u00a2\7]\2\2\u00a2\20\3\2\2")
        buf.write("\2\u00a3\u00a4\7_\2\2\u00a4\22\3\2\2\2\u00a5\u00a6\7?")
        buf.write("\2\2\u00a6\24\3\2\2\2\u00a7\u00a8\7=\2\2\u00a8\26\3\2")
        buf.write("\2\2\u00a9\u00aa\7\60\2\2\u00aa\30\3\2\2\2\u00ab\u00ac")
        buf.write("\7-\2\2\u00ac\u00ad\7?\2\2\u00ad\32\3\2\2\2\u00ae\u00af")
        buf.write("\7/\2\2\u00af\u00b0\7?\2\2\u00b0\34\3\2\2\2\u00b1\u00b2")
        buf.write("\7,\2\2\u00b2\u00b3\7?\2\2\u00b3\36\3\2\2\2\u00b4\u00b5")
        buf.write("\7\61\2\2\u00b5\u00b6\7?\2\2\u00b6 \3\2\2\2\u00b7\u00b8")
        buf.write("\7\'\2\2\u00b8\u00b9\7?\2\2\u00b9\"\3\2\2\2\u00ba\u00bb")
        buf.write("\7#\2\2\u00bb$\3\2\2\2\u00bc\u00bd\7(\2\2\u00bd\u00be")
        buf.write("\7(\2\2\u00be&\3\2\2\2\u00bf\u00c0\7~\2\2\u00c0\u00c1")
        buf.write("\7~\2\2\u00c1(\3\2\2\2\u00c2\u00c3\7A\2\2\u00c3*\3\2\2")
        buf.write("\2\u00c4\u00c9\7$\2\2\u00c5\u00c8\5-\27\2\u00c6\u00c8")
        buf.write("\n\2\2\2\u00c7\u00c5\3\2\2\2\u00c7\u00c6\3\2\2\2\u00c8")
        buf.write("\u00cb\3\2\2\2\u00c9\u00c7\3\2\2\2\u00c9\u00ca\3\2\2\2")
        buf.write("\u00ca\u00cc\3\2\2\2\u00cb\u00c9\3\2\2\2\u00cc\u00d7\7")
        buf.write("$\2\2\u00cd\u00d2\7)\2\2\u00ce\u00d1\5-\27\2\u00cf\u00d1")
        buf.write("\n\3\2\2\u00d0\u00ce\3\2\2\2\u00d0\u00cf\3\2\2\2\u00d1")
        buf.write("\u00d4\3\2\2\2\u00d2\u00d0\3\2\2\2\u00d2\u00d3\3\2\2\2")
        buf.write("\u00d3\u00d5\3\2\2\2\u00d4\u00d2\3\2\2\2\u00d5\u00d7\7")
        buf.write(")\2\2\u00d6\u00c4\3\2\2\2\u00d6\u00cd\3\2\2\2\u00d7,\3")
        buf.write("\2\2\2\u00d8\u00d9\7^\2\2\u00d9\u00da\t\4\2\2\u00da.\3")
        buf.write("\2\2\2\u00db\u00dd\5\u008fH\2\u00dc\u00db\3\2\2\2\u00dd")
        buf.write("\u00de\3\2\2\2\u00de\u00dc\3\2\2\2\u00de\u00df\3\2\2\2")
        buf.write("\u00df\60\3\2\2\2\u00e0\u00e2\5\u008fH\2\u00e1\u00e0\3")
        buf.write("\2\2\2\u00e2\u00e3\3\2\2\2\u00e3\u00e1\3\2\2\2\u00e3\u00e4")
        buf.write("\3\2\2\2\u00e4\u00e5\3\2\2\2\u00e5\u00e7\7\60\2\2\u00e6")
        buf.write("\u00e8\5\u008fH\2\u00e7\u00e6\3\2\2\2\u00e8\u00e9\3\2")
        buf.write("\2\2\u00e9\u00e7\3\2\2\2\u00e9\u00ea\3\2\2\2\u00ea\u00ec")
        buf.write("\3\2\2\2\u00eb\u00ed\5\65\33\2\u00ec\u00eb\3\2\2\2\u00ec")
        buf.write("\u00ed\3\2\2\2\u00ed\u00ff\3\2\2\2\u00ee\u00f0\7\60\2")
        buf.write("\2\u00ef\u00f1\5\u008fH\2\u00f0\u00ef\3\2\2\2\u00f1\u00f2")
        buf.write("\3\2\2\2\u00f2\u00f0\3\2\2\2\u00f2\u00f3\3\2\2\2\u00f3")
        buf.write("\u00f5\3\2\2\2\u00f4\u00f6\5\65\33\2\u00f5\u00f4\3\2\2")
        buf.write("\2\u00f5\u00f6\3\2\2\2\u00f6\u00ff\3\2\2\2\u00f7\u00f9")
        buf.write("\5\u008fH\2\u00f8\u00f7\3\2\2\2\u00f9\u00fa\3\2\2\2\u00fa")
        buf.write("\u00f8\3\2\2\2\u00fa\u00fb\3\2\2\2\u00fb\u00fc\3\2\2\2")
        buf.write("\u00fc\u00fd\5\65\33\2\u00fd\u00ff\3\2\2\2\u00fe\u00e1")
        buf.write("\3\2\2\2\u00fe\u00ee\3\2\2\2\u00fe\u00f8\3\2\2\2\u00ff")
        buf.write("\62\3\2\2\2\u0100\u0101\7v\2\2\u0101\u0102\7t\2\2\u0102")
        buf.write("\u0103\7w\2\2\u0103\u010a\7g\2\2\u0104\u0105\7h\2\2\u0105")
        buf.write("\u0106\7c\2\2\u0106\u0107\7n\2\2\u0107\u0108\7u\2\2\u0108")
        buf.write("\u010a\7g\2\2\u0109\u0100\3\2\2\2\u0109\u0104\3\2\2\2")
        buf.write("\u010a\64\3\2\2\2\u010b\u010d\t\5\2\2\u010c\u010e\t\6")
        buf.write("\2\2\u010d\u010c\3\2\2\2\u010d\u010e\3\2\2\2\u010e\u0110")
        buf.write("\3\2\2\2\u010f\u0111\5\u008fH\2\u0110\u010f\3\2\2\2\u0111")
        buf.write("\u0112\3\2\2\2\u0112\u0110\3\2\2\2\u0112\u0113\3\2\2\2")
        buf.write("\u0113\66\3\2\2\2\u0114\u0115\7e\2\2\u0115\u0116\7n\2")
        buf.write("\2\u0116\u0117\7c\2\2\u0117\u0118\7u\2\2\u0118\u0119\7")
        buf.write("u\2\2\u01198\3\2\2\2\u011a\u011b\7c\2\2\u011b\u011c\7")
        buf.write("v\2\2\u011c\u011d\7v\2\2\u011d\u011e\7t\2\2\u011e:\3\2")
        buf.write("\2\2\u011f\u0120\7u\2\2\u0120\u0121\7v\2\2\u0121\u0122")
        buf.write("\7c\2\2\u0122\u0123\7v\2\2\u0123\u0124\7g\2\2\u0124<\3")
        buf.write("\2\2\2\u0125\u0126\7h\2\2\u0126\u0127\7w\2\2\u0127\u0128")
        buf.write("\7p\2\2\u0128\u0129\7e\2\2\u0129>\3\2\2\2\u012a\u012b")
        buf.write("\7r\2\2\u012b\u012c\7t\2\2\u012c\u012d\7g\2\2\u012d\u012e")
        buf.write("\7f\2\2\u012e@\3\2\2\2\u012f\u0130\7q\2\2\u0130\u0131")
        buf.write("\7r\2\2\u0131\u0132\7g\2\2\u0132\u0133\7t\2\2\u0133B\3")
        buf.write("\2\2\2\u0134\u0135\7k\2\2\u0135\u0136\7h\2\2\u0136D\3")
        buf.write("\2\2\2\u0137\u0138\7g\2\2\u0138\u0139\7n\2\2\u0139\u013a")
        buf.write("\7k\2\2\u013a\u013b\7h\2\2\u013bF\3\2\2\2\u013c\u013d")
        buf.write("\7g\2\2\u013d\u013e\7n\2\2\u013e\u013f\7u\2\2\u013f\u0140")
        buf.write("\7g\2\2\u0140H\3\2\2\2\u0141\u0142\7h\2\2\u0142\u0143")
        buf.write("\7q\2\2\u0143\u0144\7t\2\2\u0144J\3\2\2\2\u0145\u0146")
        buf.write("\7y\2\2\u0146\u0147\7j\2\2\u0147\u0148\7k\2\2\u0148\u0149")
        buf.write("\7n\2\2\u0149\u014a\7g\2\2\u014aL\3\2\2\2\u014b\u014c")
        buf.write("\7t\2\2\u014c\u014d\7g\2\2\u014d\u014e\7v\2\2\u014eN\3")
        buf.write("\2\2\2\u014f\u0150\7d\2\2\u0150\u0151\7t\2\2\u0151\u0152")
        buf.write("\7g\2\2\u0152\u0153\7c\2\2\u0153\u0154\7m\2\2\u0154P\3")
        buf.write("\2\2\2\u0155\u0156\7e\2\2\u0156\u0157\7q\2\2\u0157\u0158")
        buf.write("\7p\2\2\u0158\u0159\7v\2\2\u0159R\3\2\2\2\u015a\u015b")
        buf.write("\7y\2\2\u015b\u015c\7j\2\2\u015c\u015d\7g\2\2\u015d\u015e")
        buf.write("\7p\2\2\u015eT\3\2\2\2\u015f\u0160\7g\2\2\u0160\u0161")
        buf.write("\7h\2\2\u0161\u0162\7h\2\2\u0162V\3\2\2\2\u0163\u0164")
        buf.write("\7g\2\2\u0164\u0165\7z\2\2\u0165\u0166\7g\2\2\u0166\u0167")
        buf.write("\7e\2\2\u0167X\3\2\2\2\u0168\u0169\7k\2\2\u0169\u016a")
        buf.write("\7p\2\2\u016a\u016b\7k\2\2\u016b\u016c\7v\2\2\u016cZ\3")
        buf.write("\2\2\2\u016d\u016e\7i\2\2\u016e\u016f\7q\2\2\u016f\u0170")
        buf.write("\7c\2\2\u0170\u0171\7n\2\2\u0171\\\3\2\2\2\u0172\u0173")
        buf.write("\7o\2\2\u0173\u0174\7c\2\2\u0174\u0175\7k\2\2\u0175\u0176")
        buf.write("\7p\2\2\u0176^\3\2\2\2\u0177\u0178\7k\2\2\u0178\u0179")
        buf.write("\7p\2\2\u0179`\3\2\2\2\u017a\u017b\7f\2\2\u017b\u017c")
        buf.write("\7q\2\2\u017c\u017d\7o\2\2\u017db\3\2\2\2\u017e\u017f")
        buf.write("\7u\2\2\u017f\u0180\7g\2\2\u0180\u0181\7v\2\2\u0181d\3")
        buf.write("\2\2\2\u0182\u0183\7t\2\2\u0183\u0184\7c\2\2\u0184\u0185")
        buf.write("\7p\2\2\u0185\u0186\7i\2\2\u0186\u0187\7g\2\2\u0187f\3")
        buf.write("\2\2\2\u0188\u0189\7n\2\2\u0189\u018a\7k\2\2\u018a\u018b")
        buf.write("\7u\2\2\u018b\u018c\7v\2\2\u018ch\3\2\2\2\u018d\u018e")
        buf.write("\7d\2\2\u018e\u018f\7q\2\2\u018f\u0190\7q\2\2\u0190\u0191")
        buf.write("\7n\2\2\u0191j\3\2\2\2\u0192\u0193\7u\2\2\u0193\u0194")
        buf.write("\7v\2\2\u0194\u0195\7t\2\2\u0195l\3\2\2\2\u0196\u0197")
        buf.write("\7h\2\2\u0197\u0198\7n\2\2\u0198\u0199\7q\2\2\u0199\u019a")
        buf.write("\7c\2\2\u019a\u019b\7v\2\2\u019bn\3\2\2\2\u019c\u019d")
        buf.write("\7k\2\2\u019d\u019e\7p\2\2\u019e\u019f\7v\2\2\u019fp\3")
        buf.write("\2\2\2\u01a0\u01a1\7p\2\2\u01a1\u01a2\7w\2\2\u01a2\u01a3")
        buf.write("\7o\2\2\u01a3r\3\2\2\2\u01a4\u01a5\7x\2\2\u01a5\u01a6")
        buf.write("\7c\2\2\u01a6\u01a7\7t\2\2\u01a7t\3\2\2\2\u01a8\u01a9")
        buf.write("\7,\2\2\u01a9v\3\2\2\2\u01aa\u01ab\7\61\2\2\u01abx\3\2")
        buf.write("\2\2\u01ac\u01ad\7\'\2\2\u01adz\3\2\2\2\u01ae\u01af\7")
        buf.write("-\2\2\u01af|\3\2\2\2\u01b0\u01b1\7/\2\2\u01b1~\3\2\2\2")
        buf.write("\u01b2\u01b3\7>\2\2\u01b3\u0080\3\2\2\2\u01b4\u01b5\7")
        buf.write("@\2\2\u01b5\u0082\3\2\2\2\u01b6\u01b7\7>\2\2\u01b7\u01b8")
        buf.write("\7?\2\2\u01b8\u0084\3\2\2\2\u01b9\u01ba\7@\2\2\u01ba\u01bb")
        buf.write("\7?\2\2\u01bb\u0086\3\2\2\2\u01bc\u01bd\7#\2\2\u01bd\u01be")
        buf.write("\7?\2\2\u01be\u0088\3\2\2\2\u01bf\u01c0\7?\2\2\u01c0\u01c1")
        buf.write("\7?\2\2\u01c1\u008a\3\2\2\2\u01c2\u01c8\5\u008dG\2\u01c3")
        buf.write("\u01c7\5\u008dG\2\u01c4\u01c7\7a\2\2\u01c5\u01c7\5\u008f")
        buf.write("H\2\u01c6\u01c3\3\2\2\2\u01c6\u01c4\3\2\2\2\u01c6\u01c5")
        buf.write("\3\2\2\2\u01c7\u01ca\3\2\2\2\u01c8\u01c6\3\2\2\2\u01c8")
        buf.write("\u01c9\3\2\2\2\u01c9\u008c\3\2\2\2\u01ca\u01c8\3\2\2\2")
        buf.write("\u01cb\u01cc\t\7\2\2\u01cc\u008e\3\2\2\2\u01cd\u01ce\t")
        buf.write("\b\2\2\u01ce\u0090\3\2\2\2\u01cf\u01d3\7%\2\2\u01d0\u01d2")
        buf.write("\n\t\2\2\u01d1\u01d0\3\2\2\2\u01d2\u01d5\3\2\2\2\u01d3")
        buf.write("\u01d1\3\2\2\2\u01d3\u01d4\3\2\2\2\u01d4\u01d6\3\2\2\2")
        buf.write("\u01d5\u01d3\3\2\2\2\u01d6\u01d7\bI\2\2\u01d7\u0092\3")
        buf.write("\2\2\2\u01d8\u01da\t\n\2\2\u01d9\u01d8\3\2\2\2\u01da\u01db")
        buf.write("\3\2\2\2\u01db\u01d9\3\2\2\2\u01db\u01dc\3\2\2\2\u01dc")
        buf.write("\u01dd\3\2\2\2\u01dd\u01de\bJ\2\2\u01de\u0094\3\2\2\2")
        buf.write("\27\2\u00c7\u00c9\u00d0\u00d2\u00d6\u00de\u00e3\u00e9")
        buf.write("\u00ec\u00f2\u00f5\u00fa\u00fe\u0109\u010d\u0112\u01c6")
        buf.write("\u01c8\u01d3\u01db\3\b\2\2")
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
    SET = 47
    RANGE = 48
    LIST = 49
    BOOL = 50
    STR = 51
    FLOAT = 52
    INT = 53
    NUM = 54
    VAR = 55
    MUL = 56
    DIV = 57
    MOD = 58
    ADD = 59
    SUB = 60
    LT = 61
    GT = 62
    LE = 63
    GE = 64
    NE = 65
    EQ = 66
    ID = 67
    COMMENT = 68
    WS = 69

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'{'", "'}'", "':'", "'('", "')'", "','", "'['", "']'", "'='", 
            "';'", "'.'", "'+='", "'-='", "'*='", "'/='", "'%='", "'!'", 
            "'&&'", "'||'", "'?'", "'class'", "'attr'", "'state'", "'func'", 
            "'pred'", "'oper'", "'if'", "'elif'", "'else'", "'for'", "'while'", 
            "'ret'", "'break'", "'cont'", "'when'", "'eff'", "'exec'", "'init'", 
            "'goal'", "'main'", "'in'", "'dom'", "'set'", "'range'", "'list'", 
            "'bool'", "'str'", "'float'", "'int'", "'num'", "'var'", "'*'", 
            "'/'", "'%'", "'+'", "'-'", "'<'", "'>'", "'<='", "'>='", "'!='", 
            "'=='" ]

    symbolicNames = [ "<INVALID>",
            "STRING_LITERAL", "DECIMAL_LITERAL", "FLOAT_LITERAL", "BOOL_LITERAL", 
            "CLASS", "ATTR", "STATE", "FUNC", "PRED", "OPER", "IF", "ELIF", 
            "ELSE", "FOR", "WHILE", "RET", "BREAK", "CONT", "WHEN", "EFF", 
            "EXEC", "INIT", "GOAL", "MAIN", "IN", "DOM", "SET", "RANGE", 
            "LIST", "BOOL", "STR", "FLOAT", "INT", "NUM", "VAR", "MUL", 
            "DIV", "MOD", "ADD", "SUB", "LT", "GT", "LE", "GE", "NE", "EQ", 
            "ID", "COMMENT", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "T__17", "T__18", "T__19", 
                  "STRING_LITERAL", "STRING_ESCAPE", "DECIMAL_LITERAL", 
                  "FLOAT_LITERAL", "BOOL_LITERAL", "EXPONENT", "CLASS", 
                  "ATTR", "STATE", "FUNC", "PRED", "OPER", "IF", "ELIF", 
                  "ELSE", "FOR", "WHILE", "RET", "BREAK", "CONT", "WHEN", 
                  "EFF", "EXEC", "INIT", "GOAL", "MAIN", "IN", "DOM", "SET", 
                  "RANGE", "LIST", "BOOL", "STR", "FLOAT", "INT", "NUM", 
                  "VAR", "MUL", "DIV", "MOD", "ADD", "SUB", "LT", "GT", 
                  "LE", "GE", "NE", "EQ", "ID", "LETTER", "DIGIT", "COMMENT", 
                  "WS" ]

    grammarFileName = "Evans.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


