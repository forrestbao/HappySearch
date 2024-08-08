def get_parse_timedtext(Mode='web', VideoID='yJXTXN4xrI8'):
    """get the XML format timedtext and parse it
    """
    if Mode == 'web':
        import urllib2
        try:
            response = urllib2.urlopen('http://video.google.com/timedtext?lang=en&v=' + VideoID)
        except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code)
            print 'Oops, either the videoid is wrong or this video has no English timed text.'
            exit() 
        except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason)
        except httplib.HTTPException, e:
            print 'HTTPException happened in HappySearch.'
        except Exception:
            import traceback
            print 'generic exception: ' + traceback.format_exc()
#    timedtext = response.read()
    else: 
        response = VideoID + ".xml"
    import xml.etree.ElementTree
    import collections
    try:
        tree =  xml.etree.ElementTree.parse(response)
    except xml.etree.ElementTree.ParseError, e:
        print "This video doesn't seem to have timed text. Here is the detailed error: ", e
        exit() 
    Times = collections.OrderedDict([(float(child.get('start')), child.text) for child in tree.getroot()])
    for Start, Line in Times.iteritems():
        print Start, Line
#    for child in tree.getroot():
#        print child.get('start'), child.get('duration'), child.text 
    return Times

def find_match(Keyword, String):
    """Given a keyword, or a combination of keywords, determine whether it matches in the String

    Notes: Currently, only the simplest case is implemented for demonstration purpose. 
    """
    if Keyword in String:
        return True
    else:
        return False

def searchkey(Keyword, Times, case_sensitive=False, debug=False):
    """Given a search key and a timed text, find all matches

    case_sensitive: Boolean, whether using case sensitive search
    Matches: ordered dict, keys as timestamp and values as str
    """
    import collections
    Times = collections.OrderedDict([(Start, Line.replace("&#39;", "'")) for Start, Line in Times.iteritems()])
    print "Searching for: ", Keyword, "..."
    if not case_sensitive:
        Times = collections.OrderedDict([(Start, Line.lower()) for Start, Line in Times.iteritems()])
        Keyword = Keyword.lower()# since we do not demo combinatorial search, this can be done easily. 

    Matches = collections.OrderedDict([(Start, Line) for Start, Line in Times.iteritems() if find_match(Keyword, Line)])

#    for Start, String in Times.iteritems():
#        if Keyword in String:
#            Matches.append((Start, String))
    if debug:
        for (Start, String) in Matches.iteritems():
           print Start, String 
    return Matches

    print "Sadly, no matching found for the query: ", Keyword
    return None


def send_play(Start, VideoID):
    m, s = divmod(Start, 60)
    print "A match found at %02d:%02d" % (m, s)
    import webbrowser
    URL= "https://youtu.be/" + VideoID + "?t=" + str(int(m)) + "m" + str(int(s)) +  "s"
    try:
        webbrowser.open_new(URL)
    except  webbrowser.Error, e:
        print e    
    print "A browser window should open for you automatically. if not, copy the URL below to your browser and start enjoying!"
    print URL
    return URL

def happy_search(VideoID, Keyword):
    """Top level function for happy search for YouTube

    Matches: dict, keys as timestamp, value as string

    Notes: This function only displays the first match 
    """
    Times = get_parse_timedtext(Mode='web', VideoID=VideoID)
    Matches = searchkey(Keyword, Times)
    Start = Matches.popitem(last=False)[0]
    if Start != None:
        URL = send_play(Start, VideoID)
        return URL
    return None

def happy_search_list(VideoID, Keyword):
    """Top level function that displays all matches
    """
    Times = get_parse_timedtext(Mode='web', VideoID=VideoID)
    Matches = searchkey(Keyword, Times)
    return Matches

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='This is Happy Search MVP! Made by Yang Liu and Sheng Bao.')
    parser.add_argument('--videoid', type=str, default='yJXTXN4xrI8',
                   help='the ID of a youtube video')
    parser.add_argument('--query', default='solution',
                   help='the search query')
    args = parser.parse_args()
    happy_search(args.videoid, args.query)

    
