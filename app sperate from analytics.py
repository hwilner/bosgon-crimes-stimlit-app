# Core Pkgs
import streamlit as st # version 0.64 


# Load EDA Pkgs
import pandas as pd 

# Load Data Viz Pkgs
import matplotlib.pyplot as plt 
import matplotlib 
matplotlib.use('Agg')
import seaborn as sns 


# General Functions
@st.cache
def load_data(data):
	df = pd.read_csv(data)
	return df 

 # Function to Find Top Offense Per Day of Week
def get_count_of_offense_per_day_of_week(offense,data):
    # Plot For Vandalism Per Day of the week
    df = data 
    plt.title("Count of Offense for {}".format(offense))
    # fig,ax = plt.subplot()
    sns.countplot(df[df['OFFENSE_CODE_GROUP'] == offense]['DAY_OF_WEEK'])
    # ax.bar(df[df['OFFENSE_CODE_GROUP'] == offense]['DAY_OF_WEEK'].value_counts())
    st.pyplot()


# Function to Get Average Serious Crime Per Month
def sns_plot_average_serious_crime(df,district,year=2016):
	serious_crimes = ["Larceny", "Robbery", "Drug Violation", "Auto Theft"]
	district_df = df[(df['DISTRICT'] == district) & (df['YEAR'] == year)]
	serious_crimes_df = district_df[district_df['OFFENSE_CODE_GROUP'].isin(serious_crimes)]
	total_crime_per_month = pd.DataFrame(serious_crimes_df.groupby('MONTH')['OFFENSE_CODE_GROUP'].value_counts().to_frame('counts').reset_index())
	avg_crime_per_month = total_crime_per_month.groupby('MONTH')['counts'].mean().to_frame('average').reset_index()
	plt.title("District:: {} Average Crime Per Month for Year :{}".format(district,year))
	sns.barplot(x='MONTH',y='average',data=avg_crime_per_month)
	st.pyplot()



def main():
	"""## Main Boston Crime App

	Enables the user to select between different pages like 'Task 1', 'Task 2','Task 3' and 'About'.
	"""
	
	menu = ["Task 1","Task 2","Task 3","About"]
	choice = st.sidebar.selectbox('Menu',menu)

	if choice == 'Task 2':
		st.subheader("Count of Offense Per Day")
		df = load_data('data/count_per_week_crime_data.csv')
		st.dataframe(df.head(10))
		
		list_of_crimes = df['OFFENSE_CODE_GROUP'].unique().tolist()

		offense_type = st.selectbox('Offense Type',list_of_crimes)
		get_count_of_offense_per_day_of_week(offense_type,df)
		st.pyplot()



	elif choice == 'Task 3':
		st.subheader('Average Count of Serious Crimes Per Month')
		df = load_data('data/serious_crime_for_2016_n_2017_crime_data.csv')
		st.dataframe(df.head())
		district_list = df['DISTRICT'].unique().tolist()
		district_choice = st.selectbox('District',district_list)
		sns_plot_average_serious_crime(df,district_choice,year=2016)
		sns_plot_average_serious_crime(df,district_choice,year=2017)



	elif choice == 'Task 1':
		st.subheader("Map Plot of Crimes Per Hour ")
		df = load_data('data/crime_per_hour_boston.csv')
		st.dataframe(df.head(10))
		hour_list = df['HOUR'].unique().tolist()
		hour_choice = st.slider('Hour',0,23)

		import pydeck as pdk
		new_df = df[df['HOUR'] == hour_choice]


		st.pydeck_chart(pdk.Deck(
		    map_style='mapbox://styles/mapbox/light-v9',
		    initial_view_state=pdk.ViewState(
		        latitude=42.361145,
		        longitude=-71.057083,
		        zoom=11,
		        pitch=50,
		    ),
		    layers=[
		        pdk.Layer(
		            'ScatterplotLayer',
		            data=new_df,
		            pickable=True,
		            opacity=0.8,
		            stroked=True,
		            filled=True,
		            radius_scale=5,
		            radius_min_pixels=1,
		            radius_max_pixels=10,
		            get_position='[Long,Lat]',
		            get_color='[200, 30, 0, 160]',
		            get_radius='counts',
		        ),
		    ],
		))



	else:
		st.subheader("About")
		html_header_temp = """
			<div style="background-color:{};padding:10px;border-radius:10px">
			<h1 style="color:{};text-align:center;">Boston Crime Analysis App </h1>
			</div>
			"""
		html_app_info_temp = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


		st.markdown(html_header_temp.format('royalblue','white'),unsafe_allow_html=True)

		app_info = """The objective of the app is to analyze and explore the crime rate in Boston via A Map Plot ,
		Bar Charts of serious crimes per week,month and hour"""


		st.markdown(html_app_info_temp.format(app_info),unsafe_allow_html=True)





if __name__ == '__main__':
	main()