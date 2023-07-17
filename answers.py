
def manager(text, state, df, pd):

    # //////////////////////////////////////////////////////////////////////////////////////////////
    if text == "Show price":
        if not pd.isnull(list(df[df["title"]=="show_price_image_path"]["message"])[0]):
            return [1, list(df[df["title"]=="show_price_image_path"]["message"])[0], list(df[df["title"]=="show_price_message"]["message"])[0]]
        elif not pd.isnull(list(df[df["title"]=="show_price_video_path"]["message"])[0]):
            return [2, list(df[df["title"]=="show_price_video_path"]["message"])[0], list(df[df["title"]=="show_price_message"]["message"])[0]]
        else:
            return [0, list(df[df["title"]=="show_price_message"]["message"])[0]]

    # //////////////////////////////////////////////////////////////////////////////////////////////
    elif text == "How to connect":
        if not pd.isnull(list(df[df["title"]=="how_to_connect_image_path"]["message"])[0]):
            return [1, list(df[df["title"]=="how_to_connect_image_path"]["message"])[0], list(df[df["title"]=="how_to_connect_message"]["message"])[0]]
        elif not pd.isnull(list(df[df["title"]=="how_to_connect_video_path"]["message"])[0]):
            return [2, list(df[df["title"]=="how_to_connect_video_path"]["message"])[0], list(df[df["title"]=="how_to_connect_message"]["message"])[0]]
        else:
            return [0, list(df[df["title"]=="how_to_connect_message"]["message"])[0]]
    
    # //////////////////////////////////////////////////////////////////////////////////////////////
    elif text == "Connect to Support":
        return [0, list(df[df["title"]=="connect_to_support_message"]["message"])[0]]

    # //////////////////////////////////////////////////////////////////////////////////////////////
    elif text == "Rules and QA":
        if not pd.isnull(list(df[df["title"]=="rules_and_qa_video_path"]["message"])[0]):
            return [3, list(df[df["title"]=="rules_and_qa_video_path"]["message"])[0], list(df[df["title"]=="rules_and_qa_message"]["message"])[0]]
        return [0, list(df[df["title"]=="rules_and_qa_message"]["message"])[0]]

    # //////////////////////////////////////////////////////////////////////////////////////////////
    else:
        return [0, "We dont undrastand your message."]
