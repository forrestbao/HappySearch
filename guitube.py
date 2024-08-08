import Tkinter

def happy_search_display(vid, query):
    """Takes in the vid and query and to display the search result
    """
    import baotube
    URL = baotube.happy_search(vid, query)
    for Element in result_frame.grid_slaves():
        Element.grid_forget() # Clear the result of previous search

    if URL != None:
        Result_prompt = Tkinter.Label(result_frame, text="Here is the beef!", bg="orange").grid(row=4, column=2)
        URL_widget = Tkinter.Text(result_frame, height=1, width=50, fg="orange")
        URL_widget.insert(1.0, URL)
        URL_widget.grid(row=5, column=2)
#        selectable.configure(inactiveselectbackground=w.cget("selectbackground"))
        URL_widget.configure(state="disabled")
    else:
        Result_prompt = Tkinter.Label(result_frame, text="The query is not found!", bg="yellow").grid(row=4, column=2)

def happy_search_list_display(vid, query):
    """An improvement to happy_search_display. Now returns a list of matches. 
    
    Matches: dict, keys as timestamp, value as string
    """
    import baotube

    for Element in result_frame.pack_slaves():
        Element.pack_forget() # Clear the result of previous search
    
    Matches = baotube.happy_search_list(vid, query)
    if len(Matches) != 0: # at least one match found
        Result_prompt = Tkinter.Label(result_frame, text="Click a button below to enjoy", bg="orange")
        Result_prompt.pack(side="top")
        for Start, Line in Matches.iteritems():
            Min, Sec = divmod(Start, 60)
            Tkinter.Button(result_frame, bg="white", text="%dm%ds: %s"%(Min, Sec,Line), command=lambda: baotube.send_play(Start, vid)).pack(side="top")
    else: 
        Result_prompt = Tkinter.Label(result_frame, text="Oops, no matches", bg="yellow")
        Result_prompt.pack(side="top")

if __name__ == "__main__":
    import baotube

#    import tkFont
#    default_font = tkFont.nametofont("TkDefaultFont")
#    default_font.configure(size=48)

    root = Tkinter.Tk()
    root.title("Happy Search by Happy Lab.")
    root.minsize(width=500, height=700)
    root.option_add("*Font", "courier 15")

    topframe = Tkinter.Frame(root, borderwidth=2)
    topframe.pack(expand = 1, pady = 5, padx = 5)
    midframe = Tkinter.Frame(root, borderwidth=6, relief="raise")
    midframe.pack(expand=1, pady = 5, padx = 5)

    header = Tkinter.Label(topframe, text="Welcome to Happy Search. \n Powered by Happy L(iu)A(nd)B(ao). \n Patents Pending. ").grid(row=0, columnspan=2, )

    # The search box
    Tkinter.Label(midframe, text="YouTube video ID:").grid(row=1, column=1)
    Tkinter.Label(midframe, text="search query:").grid(row=2, column=1)

    # a child of the midframe, the result frame
    result_frame = Tkinter.Frame(midframe, borderwidth=6, relief="sunken")
    result_frame.grid(row=4, column=1, columnspan=3, sticky="WE", pady=4)

    vid = Tkinter.Entry(midframe, width=40)
    vid.insert(Tkinter.END, "yJXTXN4xrI8")
    vid.grid(row=1, column=2, columnspan=2)

    query = Tkinter.Entry(midframe, width=40)
    query.insert(Tkinter.END, "the bRaIn")
    query.grid(row=2, column=2, columnspan=2)

    Tkinter.Button(midframe, text='Quit', command=root.quit).grid(row=3, column=2, sticky="W", pady=4)
#    Tkinter.Button(root, text='Test', command=lambda: print_entry(box2)).grid(row=3, column=1, sticky="W", pady=4)
    Tkinter.Button(midframe, text='Search', command=lambda: happy_search_list_display(vid.get(), query.get())).grid(row=3, column=3, sticky="WE", pady=4)



#    Tkinter.Button(midframe, text='Search', command=lambda: baotube.happy_search(vid.get(), query.get())).grid(row=3, column=3, sticky="W", pady=4)
   # End of the search box


    Tkinter.mainloop( )
