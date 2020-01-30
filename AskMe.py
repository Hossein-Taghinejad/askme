import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash()

data=pd.read_csv("data.csv")
reg=np.array(['Canada', 'LATAM', 'United States', 'Australia & SEA', 'India',
       'Japan', 'Central and Southern Europe', 'Eurasia',
       'French, Netherlands & Nordics', 'MENA', 'UK', 'UK - Majors'])

thet=np.array(['Americas', 'APAC', 'EMEA', 'Major Accounts', 'Other',
       'Strategic Resellers'])
cols=['Closed', 'Pipeline', 'Weighted', 'ClosedToTarget']

q=[]
ans1=[]
for i in reg:
    for j in cols:
        if j=="ClosedToTarget":
            q.append("what is my {0} for {1}".format(j, i))
            if data.Pacing[data.Region==i].values[0]==0:
                ans1.append("unfortunately, the {0} for {1} is {2} percent".format(j, i, (eval("data.{0}[data.Region=='{1}'].values[0]".format(j, i)))))
            elif data.Pacing[data.Region==i].values[0]==1:
                ans1.append("my {0} for {1} is {2} percent".format(j, i, (eval("data.{0}[data.Region=='{1}'].values[0]".format(j, i)))))
            else:
                ans1.append("congratulation, the {0} for {1} is {2} percent".format(j, i, (eval("data.{0}[data.Region=='{1}'].values[0]".format(j, i)))))
        else:
            q.append("what is my {0} for {1}".format(j,i))
            ans1.append("my {0} for {1} is {2}".format(j,i,(eval("data.{0}[data.Region=='{1}'].values[0]".format(j,i)))))

qq=[]
ans2=[]

for i in thet:
    for j in cols:
        if j == "ClosedToTarget":
            qq.append("what is my {0} for {1}".format(j, i))
            if data.Pacing[(data.Theatre == i)&(pd.isna(data.Region))].values[0] == 0:
                ans2.append("unfortunately, the {0} for {1} is {2} percent".format(j, i, (eval("data.{0}[(data.Theatre=='{1}') & (pd.isna(data.Region))].values[0]".format(j, i)))))
            elif data.Pacing[(data.Theatre == i)&(pd.isna(data.Region))].values[0] == 1:
                ans2.append("my {0} for {1} is {2} percent".format(j, i, (eval("data.{0}[(data.Theatre=='{1}') & (pd.isna(data.Region))].values[0]".format(j, i)))))
            else:
                ans2.append("congratulation, the {0} for {1} is {2}".format(j, i, (eval("data.{0}[(data.Theatre=='{1}') & (pd.isna(data.Region))].values[0]".format(j, i)))))
        else:
            qq.append("what is my {0} for {1}".format(j,i))
            ans2.append("my {0} for {1} is {2}".format(j, i, (eval("data.{0}[(data.Theatre=='{1}') & (pd.isna(data.Region))].values[0]".format(j, i)))))

qqq=["What is my total sales","What is the best Theatre","What is the worst Theatre","what is my sale rank by theatre"]
ans3=["The total sale is {0}".format(33770026.82),"The best Theatre is {0}".format("EMEA"),"The worst Theatre is {0}".format("APAC")]

questions=q+qq+qqq
answers=ans1+ans2+ans3

#-----------------------------------

def sentc(a):
    b = list(itertools.product(a, questions))
    l=[fuzz.partial_ratio(i[0],i[1]) for i in b]
    res=b[np.argmax(l)]
    return(res,max(l))


def evall(qq):
    audio = gTTS(text=qq, lang="en", slow=False)
    audio.save("welcome.mp3")
    p = vlc.MediaPlayer("welcome.mp3")
    p.play()
    current_state = p.get_state()
    while current_state != vlc.State.Ended:
        current_state = p.get_state()
    audio = gTTS(text="is this your question, Please answer by yes or no", lang="en", slow=False)
    audio.save("welcome.mp3")
    p = vlc.MediaPlayer("welcome.mp3")
    p.play()
    current_state = p.get_state()
    while current_state != vlc.State.Ended:
        current_state = p.get_state()
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    ans = r.recognize_google(audio)
    return(ans)



def speach2query():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("ask")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    question = r.recognize_google(audio,show_all=True).get("alternative")
    question=[i.get("transcript") for i in question]
    qq,score=sentc(question)
    question = qq[0]
    qq = qq[1]
    if score>85:
        ev="yes"
    else:
        ev = evall(qq)
    if ev=="yes":
        if qq=="what is my sale rank by theatre":
            return(qq)
        else:
            res = answers[questions.index(qq)]
            audio = gTTS(text=res, lang="en", slow=False)
            audio.save("welcome.mp3")
            p = vlc.MediaPlayer("welcome.mp3")
            p.play()
            return (res)

    else:
        print("Please rerun the function for your next question")
        return





#-----------------------------

app.layout = html.Div([
    html.Button(type='Submit', id='button',children="Ask SOTI",n_clicks=0),
    html.Div(id='container',children='Click Ask-SOTI button to start'),
    html.Div(dcc.Graph(id='empty', figure={'data': []}), style={'display': 'none'})
])

@app.callback(
    dash.dependencies.Output('container', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def update_output(n_clicks):
    ans=speach2query()
    if ans=="what is my sale rank by theatre":
        d=data[pd.isna(data.Region)]
        d = d[["Theatre", "ClosedToTarget"]]
        d = d[d.Theatre != "Other"]
        d=d.sort_values(["ClosedToTarget"])
        g=dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': d.Theatre.values.tolist(), 'y': d.ClosedToTarget.values.tolist(), 'type': 'bar', 'name': 'ClosedToTarget'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
        return html.Div(g)
    else:
        return(ans)

if __name__ == '__main__':
    app.run_server()