import json
import matplotlib.pyplot as plt
import pandas as pd
from pandas.io.json import json_normalize
from matplotlib.patches import Arc, Rectangle, ConnectionPatch
import networkx as nx 
import seaborn as sns

lst_player_names=[]
fixture="CRO-ENG"
def get_player_names():
	df_player_names=df[(df["type_name"]=="Starting XI")]["tactics_lineup"]
	#print(type(df_player_names.count()))
	a=int(df_player_names.count())
	#print(df_player_names[0])
	#print(type(a))
	df_player_names_croatia=[df_player_names[0][i]['player']['id'] for i in range(0,len(df_player_names[0]))]
	df_player_names_england=[df_player_names[1][i]['player']['id'] for i in range(0,len(df_player_names[1]))]
	return (df_player_names,df_player_names_england)

def heatMap(res,country):
	fig, ax = plt.subplots(figsize=(50, 50))
	colormap = sns.diverging_palette(250, 10, as_cmap=True)
	sns.heatmap(res, cmap=colormap, annot=True, fmt=".2f")
	plt.xticks(range(len(res.columns)), lst_player_names)
	plt.xticks(rotation=90)
	plt.yticks(range(len(res.columns)), lst_player_names)
	plt.yticks(rotation=0)
	plt.title("Pass Distribution Analysis - "+country+"("+fixture+")")
	plt.show()

def preprocess_data(country):
	df_pass=df[(df["type_name"]=="Pass")&(df["team_name"]==country)]["player_id"]
	df_pass.dropna(inplace=True),
	pass_ply=[int(item) for item in df_pass]
	#print(pass_ply)
	set_pass_ply=set(pass_ply)
	#print(set_pass_ply)
	df_receive=df[(df["type_name"]=="Pass")&(df["team_name"]==country)] ["pass_recipient_id"]
	df_receive.dropna(inplace=True),
	rec_ply=[int(item) for item in df_receive]

	set_rec_ply=set(rec_ply)
	lst=[]
	lst_temp=[]
	for item1 in list(set_pass_ply):	
		lst_temp_2=[]
		for item2 in list(set_rec_ply):
			df_test=df[(df["type_name"]=="Pass")&(df["team_name"]==country)&(df["player_id"]==item1)&(df["pass_recipient_id"]==item2)][["player_id","pass_recipient_id"]]
			lst_temp_2.append(len(df_test))
		lst_temp.append(lst_temp_2)
	#print(lst_temp)


	res = pd.DataFrame(lst_temp,columns=list(set_pass_ply))
	if country=="Croatia":
		global lst_player_names
		lst_player_names=['M.Mandžukić','I.Perišić','J.Pivarić','V.Ćorluka','D.Lovren','I.Strinić','D.Subašić','Š.Vrsaljko','A.Kramarić','L.Modrić','A.Rebić','D.Vida','M.Brozović','I.Rakitić']

	else:
		lst_player_names=['R.Sterling','K.Walker','H.Maguire','D.Rose','H.Kane','K.Trippier','J.Stones','J.Pickford','J.Henderson','E.Dier','J.Vardy','D.Alli','M.Rashford','A.Young','J.Lingard']
	return res



with open('Cro_England.json') as data_file:
	data=json.load(data_file)
df=json_normalize(data,sep="_")
df_cro,df_eng=get_player_names()
print(df_cro[0])
res=preprocess_data("Croatia")
heatMap(res,"Croatia")
# res=preprocess_data("England")
# heatMap(res,"England")

#print(df.columns)
def draw_pitch(ax):
	Pitch=Rectangle([0,0],width=120,height=80,fill=False)
	LeftPenalty=Rectangle([0,22.3],width=14.6,height=35.3,fill=False)
	RightPenalty=Rectangle([105.4,22.3],width=14.6,height=35.3,fill=False)
	midLine=ConnectionPatch([60,0],[60,80],"data","data")

	LeftSixYard=Rectangle([0,32],width=4.9,height=16,fill=False)
	RightSixYard=Rectangle([115.1,32],width=4.9,height=16,fill=False)
	
	centreCircle=plt.Circle((60,40),8.1,color="black",fill=False)
	centreSpot = plt.Circle((60,40),0.71,color="black")
	leftPenSpot=plt.Circle((9.7,40),0.71,color="black",fill=False)
	rightPenSpot=plt.Circle((110.3,40),0.71,color="black",fill=False)
	leftArc = Arc((9.7,40),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="black")
	rightArc = Arc((110.3,40),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="black")

	element=[Pitch,LeftPenalty,RightPenalty,LeftSixYard,RightSixYard, midLine,centreCircle, centreSpot, leftPenSpot,rightPenSpot, leftArc,rightArc]
	for i in element:
		ax.add_patch(i)


# #plt.show()

df_areas_covered_Domagoj_Vida=df[(df["player_id"]==5469)][["id", "type_name","period", "timestamp", "location"]]
df_areas_covered_Domagoj_Vida.dropna(inplace=True)
#print(df_areas_covered_Domagoj_Vida.head())
fig=plt.figure()
fig.set_size_inches(7,5)
ax=fig.add_subplot(1,1,1) # 1x1 grid 1st subplot
draw_pitch(ax)
plt.ylim(-2, 82)
plt.xlim(-2, 122)
plt.axis('off')
coords=list(df_areas_covered_Domagoj_Vida["location"])
print(coords)
x_coords=[i[0] for i in coords]
y_coords=[i[1] for i in coords]
sns.kdeplot(x_coords, y_coords, shade = "True", color = "Green", n_levels = 30)
plt.title("Heat Map for Marcelo Brozović (CRO-ENG)")
plt.show()





