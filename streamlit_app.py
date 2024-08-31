
import streamlit as st
from pytubefix import YouTube
from io import BytesIO
import os
import time


def housekeeping(file):
    os.remove(f'./{file}')
    time.sleep(5)
    st.write('File successfully downloaded!')


def down_vid(yt):
    res_mp4files = yt.streams.get_highest_resolution()
    if res_mp4files:
        filename = res_mp4files.default_filename

        try:
            res_mp4files.download('./', filename)

            with open(f'./{filename}', 'rb') as fh:
                buf = BytesIO(fh.read())
            fh.close()

            if st.download_button('Download Video', data=buf, file_name=filename, mime='video/mp4'):
                housekeeping(filename)

        except Exception as down_err:
            st.write(f'Error is: {down_err}')


def down_aud(yt):
    res_mp4files = yt.streams.get_audio_only()
    if res_mp4files:
        filename = res_mp4files.default_filename

        try:
            res_mp4files.download('./', filename)

            with open(f'./{filename}', 'rb') as fh:
                buf = BytesIO(fh.read())
            fh.close()

            if st.download_button('Download Audio', data=buf, file_name=filename, mime='audio/mp4'):
                housekeeping(filename)

        except Exception as down_err:
            st.write(f'Error is: {down_err}')


def fetch_mp4_files(link):
    try:
        # object creation using YouTube
        # which was imported in the beginning
        yt = YouTube(link)
        #yt = YouTube(link, on_progress_callback=st.progress)
        # get the video with the extension and
        # filter out all the files with "mp4" extension

        # st.write('Video/Audio is available for download!!')
        st.write('Choose Video or Audio to download:')

        option = st.radio('Choose Video or Audio to download:', options=('Video', 'Audio'))

        if option == 'Video':
            down_vid(yt)
        elif option == 'Audio':
            down_aud(yt)

    except Exception as conn_err:
        st.write(f'Connection error: {conn_err}')  # to handle exception


def set_config():
    # setting page icon
    st.set_page_config(page_title='Download YouTube Video/Audio',
                       page_icon='timer_clock', initial_sidebar_state='auto')

    # hide hamburger menu and footer logo
    hide_st_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        </style>
                        """
    st.markdown(hide_st_style, unsafe_allow_html=True)


def get_link():
    dlink = st.text_input('Enter YouTube link here:', help='Enter YouTube link to be downloaded',
                          placeholder='Enter YouTube link here')
    if dlink:
        fetch_mp4_files(dlink)


def download_app():
    set_config()
    get_link()


if __name__ == '__main__':
    download_app()

