
import webview

webview.create_window(
    title='Ayat',
    url='https://ayat.chbkn.dev/',
    width=1300,
    height=1000,
    x=310,
    y=25,
    resizable=True,
    fullscreen=False,
    min_size=(500, 1000),
)

webview.start(debug=False, gui='edgechromium', private_mode=False, icon='icon_splashxxxhdpi.ico')
