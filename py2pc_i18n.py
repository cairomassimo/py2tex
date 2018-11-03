from py2pc import Keywords

class UnicodeKeywords(Keywords):
    ASSIGN = "←"

class ItalianKeywords(Keywords):
    IF = "se"
    THEN = "allora"
    ELSE = "altrimenti"
    ENDIF = "fine"
    WHILE = "finché"
    REPEAT = "ripeti"
    ENDWHILE = "fine"
    RETURN = "ritorna"

lang = {
    "it": ItalianKeywords,
}