
# coding: utf-8

# In[204]:

import pandas as pd
star_wars = pd.read_csv("star_wars.csv",encoding = "ISO-8859-1")
star_wars.head(10)


# In[205]:

star_wars.columns


# In[192]:

star_wars["RespondentID"].dropna().shape[0]


# In[193]:

star_wars["RespondentID"][pd.isnull(star_wars["RespondentID"])]


# In[195]:

star_wars["RespondentID"][pd.notnull(star_wars["RespondentID"])].shape[0]


# In[196]:

pd.notnull(star_wars["RespondentID"])


# In[197]:

star_wars = star_wars[pd.notnull(star_wars["RespondentID"])]
star_wars.head()


# In[198]:

yes_no = {"Yes" : True,"No" :False}
star_wars = star_wars["Have you seen any of the 6 films in the Star Wars franchise?"].map(yes_no)
star_wars.head()


# In[206]:

cols = star_wars.columns[1:3]
yes_no = {"Yes" : True,"No" :False}
for col in cols:
    star_wars[col] =  star_wars[col].map(yes_no)
star_wars.head()


# In[207]:

import numpy as np 
movie = {
    "Star Wars: Episode I  The Phantom Menace": True,
    np.nan:False,
    "Star Wars: Episode II  Attack of the Clones": True,
    "Star Wars: Episode III  Revenge of the Sith": True,
    "Star Wars: Episode IV  A New Hope": True,
    "Star Wars: Episode V The Empire Strikes Back": True,
    "Star Wars: Episode VI Return of the Jedi": True
}
#series methods:
cols = star_wars.columns[3:9]
for col in cols:
    star_wars[col] =star_wars[col].map(movie)
star_wars.head()


# In[208]:


star_wars = star_wars.rename(columns = {"Which of the following Star Wars films have you seen? Please select all that apply.": "seen_1",
        "Unnamed: 4": "seen_2",
        "Unnamed: 5": "seen_3",
        "Unnamed: 6": "seen_4",
        "Unnamed: 7": "seen_5",
        "Unnamed: 8": "seen_6"})
star_wars.head()


# In[274]:

star = star_wars[star_wars.columns[9:15]].astype(float)


# In[210]:

star_wars = star_wars.rename(columns = {'Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.' : "ranking_1",
       'Unnamed: 10' : "ranking_2", 'Unnamed: 11' : "ranking_3", 'Unnamed: 12' : "ranking_4", 'Unnamed: 13' : "ranking_5",
       'Unnamed: 14' : "ranking_6"})
star_wars.head()


# In[211]:

a = star_wars[star_wars.columns[9:15]].dropna().loc[1:,:].astype(float).mean()


# In[212]:

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
plt.bar(range(6),a)
plt.xticks(range(6),a.index,rotation = 90)
plt.show()


# In[214]:

b = star_wars[star_wars.columns[3:9]].sum()


# In[215]:

plt.bar(range(6),b)
plt.xticks(range(6),b.index)
plt.show()


# In[234]:

males = star_wars[star_wars["Gender"] == "Male"]
females =star_wars[star_wars["Gender"] == "Female"]
aa = males[males.columns[9:15]].dropna().astype(float).mean()
bb  =females[males.columns[9:15]].dropna().astype(float).mean()
aaa = males[males.columns[3:9]].sum()
bbb  =females[females.columns[3:9]].sum()
print(aa)
print(bb)
print(aaa)
print(bbb)


# In[233]:

males = star_wars[star_wars["Gender"] == "Male"]
males[males.columns[9:15]].dropna().astype(float).mean()


# In[250]:

plt.bar(range(6),aa)
plt.xticks(range(6),aa.index)
plt.show()


# In[256]:

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax1.bar(range(6),aa)
ax1.set(ylim = (0,4.5),yticklabels =([0,0.5,1,1.5,2,2.5,3,3.5,4,4.5]),xlim = (0,6),xticklabels = ([0,1,2,3,4,5]) )

plt.show()


# In[272]:

fig = plt.figure(figsize = (8,8))
ax1 = fig.add_subplot(2,2,1)
ax1.bar(range(6),aa)
ax1.set_ylabel("male rankings")
ax2  =fig.add_subplot(2,2,2)
ax2.bar(range(6),bb)
ax2.set_ylabel("females ranking")
ax3  =fig.add_subplot(2,2,3)
ax3.bar(range(6),aaa)
ax3.set_ylabel("male counts")
ax4  =fig.add_subplot(2,2,4)
ax4.bar(range(6),bbb)
#ax4.get_yaxis().set_visible(False)
ax4.set_ylabel("female counts")
plt.show()


# In[ ]:



