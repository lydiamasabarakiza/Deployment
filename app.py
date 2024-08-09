import joblib
import numpy as np
import pandas as pd
import streamlit as st
import base64
import smtplib
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set page configuration
st.set_page_config(page_title="Predictive Model Web App", layout="wide")

# Load the necessary encoders and models
dummies_columns = joblib.load(r'C:\Users\lydia\OneDrive\Desktop\App\dummies_columns.joblib')
le = joblib.load(r'C:\Users\lydia\OneDrive\Desktop\App\label_encoder.joblib')
scaler = joblib.load(r'C:\Users\lydia\OneDrive\Desktop\App\scaler.joblib')
model = joblib.load(r'C:\Users\lydia\OneDrive\Desktop\App\xgboost_model.save')

# Function to convert the local image file to a base64 string
def get_base64_image(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")

# Function to preprocess input data
def preprocess_input(data):
    # Create DataFrame with the new data
    X_input = pd.DataFrame([data], columns=columns)
    
    # Reorder columns to ensure consistent column order
    X_input = X_input[columns]
    
    # Feature encoding
    X_encoded = pd.get_dummies(X_input, drop_first=True)
    
    # Align columns with model training data
    X_encoded = X_encoded.reindex(columns=dummies_columns, fill_value=0)
    
    # Feature scaling
    X_scaled = scaler.transform(X_encoded)
    
    return X_scaled

def save_feedback_to_sheet(feedback):
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    # Add your service account JSON file here
    creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\lydia\Downloads\pneumonia-prediction-431920-2b37c0c52c18.json", scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open("Feedback Form").sheet1  # Open the sheet named "Feedback"

    # Add the feedback to the sheet
    sheet.append_row([feedback])

def load_dashboard():
    st.markdown(
        """
        <iframe title="Hospital_Analysis" width="600" height="373.5" 
        src="https://app.powerbi.com/view?r=eyJrIjoiMzY3OWIzYTctYWFiOC00MzI5LWI5ZGYtZWE0MWJkMTM5YmM5IiwidCI6IjE2ZDgzZWU2LTI1NGEtNDY5ZC1hNmNjLTU0ZTJjYTIzMTNlNyIsImMiOjh9" 
        frameborder="0" allowFullScreen="true"></iframe>
        """, 
        unsafe_allow_html=True
    )

# Sidebar for navigation
st.sidebar.title("Menu")
selection = st.sidebar.radio("Go to", ["Home", "Predictive Model", "Dashboard", "Feedback"])

st.session_state.page = selection

# Convert the image to base64
image_base64 = get_base64_image("C:/Users/lydia/Downloads/pneumoniap.jpg")

# Title of the application
# st.title('Pneumonia Mortality Prediction')


# Initializing session state
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Home Page
if st.session_state.page == "Home":

    # Apply CSS for styling with the header background image
    st.markdown(
        f"""
        <style>
        /* Header section with the background image */
        .header {{
            background: url('data:image/jpg;base64,{image_base64}') no-repeat center center;
            background-size: cover;
            color: #ffffff;
            height: 250px; /* Set the height for the header */
            width: 100%;
            margin: 0;
            padding: 0; /* Remove any default padding */
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        /* Add an overlay to the header */
        .header-overlay {{
            background-color: rgba(0, 0, 0, 0.5); /* Black overlay with 50% opacity */
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }}

        /* Styling for header content */
        .header-content {{
            position: relative;
            z-index: 1;
            text-align: center;
            color: #ffffff;
            padding: 20px; /* Add padding to space out the content */
        }}

        /* General text color and styling */
        body, .stMarkdown, .center-title, .content, .sidebar-content, .sidebar-text {{
            color: #ffffff;
        }}

        /* Styling for the rest of the page */
        .content-container {{
            padding: 20px;
            background-color: #333333; /* Set a background color for the main content */
            color: #ffffff; /* White text for readability */
        }}

        /* Title styling */
        h1, h2, h3, h4, h5, h6 {{
            color: #ffffff; /* All headers to be white */
            margin: 10px 0; /* Add margin to separate headers */
        }}
        
        /* Remove default margins and padding to prevent unwanted spacing */
        .header-content h1, .header-content p {{
            margin: 0;
            padding: 0;
        }}
        
        /* Additional styling for paragraphs */
        p {{
            line-height: 1.5; /* Set line height for better readability */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create the header with the background image and overlay
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.markdown('<div class="header-overlay"></div>', unsafe_allow_html=True)
    st.markdown('<div class="header-content">', unsafe_allow_html=True)
    st.markdown('<h1>Pneumonia Mortality Prediction</h1>', unsafe_allow_html=True)
    st.markdown('<p>Your tagline or description goes here.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Main content area
    st.markdown('<div class="content-container">', unsafe_allow_html=True)

    # Key Features Section
    st.header('Key Features')

    # Your main content with styling
    st.markdown('<h3 style="color: #ffffff;">Real-time Predictions</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #ffffff;">Get accurate predictions in real-time using our advanced model.</p>', unsafe_allow_html=True)

    st.markdown('<h3 style="color: #ffffff;">Data Visualization</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #ffffff;">Visualize your data and predictions with interactive charts and graphs.</p>', unsafe_allow_html=True)

    st.markdown('<h3 style="color: #ffffff;">Model Insights</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #ffffff;">Gain insights into the model’s performance and decision-making process.</p>', unsafe_allow_html=True)

    # End of the main content area
    st.markdown('</div>', unsafe_allow_html=True)

    # Contact Information Section
    st.header('Contact Us')
    st.write('For any inquiries, please contact us at: **infofeedback@gmail.com**')

    # Model Report Section
    st.header('Model Report')
    st.write('For detailed information about how the model was built, please refer to the report')

elif st.session_state.page == "Feedback":
    st.title("Feedback")
    st.subheader("We'd Love Your Feedback!")
    
    feedback = st.text_area("Please share your thoughts or suggestions:", "")
    
    if st.button("Submit Feedback"):
        if feedback:
            save_feedback_to_sheet(feedback)
            st.success("Thank you for your feedback!")
        else:
            st.error("Please enter some feedback before submitting.")



elif st.session_state.page == "Predictive Model":
    st.title("Risk of Mortality Prediction")
    st.markdown("Model to classify patient's risk of mortality from pneumonia")
    
    labels = ['Minor', 'Moderate', 'Major', 'Extreme']
    columns = ['Health Service Area', 'Hospital County', 'Facility Name', 'Age Group',
               'Zip Code - 3 digits', 'Gender', 'Race', 'Ethnicity', 'Length of Stay',
               'Type of Admission', 'Patient Disposition', 
               'CCS Diagnosis Code', 'CCS Diagnosis Description', 'CCS Procedure Code',
               'CCS Procedure Description', 'APR DRG Code', 'APR DRG Description',
               'APR MDC Code', 'APR MDC Description', 'APR Severity of Illness Code',
               'APR Severity of Illness Description',
               'APR Medical Surgical Description', 
               'Payment Typology 1']

    # Collect user inputs
    health_service_area = st.selectbox('Health Service Area', 
        ['', 'Capital/Adiron', 'Western NY', 'Central NY', 'Southern Tier',
         'Finger Lakes', 'Hudson Valley', 'Long Island', 'New York City'])

    hospital_county = st.selectbox('Hospital County',
        ['', 'Albany', 'Allegany', 'Broome', 'Cattaraugus', 'Cayuga', 'Chautauqua', 'Chemung', 'Chenango', 
         'Clinton', 'Columbia', 'Cortland', 'Delaware', 'Dutchess', 'Erie', 'Suffolk', 'Essex', 'Franklin', 
         'Fulton', 'Genesee', 'Herkimer', 'Jefferson', 'Lewis', 'Livingston', 'Madison', 'Monroe', 
         'Montgomery', 'Nassau', 'Niagara', 'Oneida', 'Onondaga', 'Ontario', 'Orange', 'Orleans', 'Oswego', 
         'Otsego', 'Putnam', 'Rensselaer', 'Rockland', 'St Lawrence', 'Saratoga', 'Schenectady', 'Schoharie', 
         'Schuyler', 'Steuben', 'Sullivan', 'Tompkins', 'Ulster', 'Warren', 'Wayne', 'Westchester', 'Wyoming', 
         'Yates', 'Bronx', 'Kings', 'Manhattan', 'Queens', 'Richmond'])

    facility_name = st.selectbox('Facility Name',
        ['', 'Albany Medical Center Hospital', 'Albany Memorial Hospital', 'St Peters Hospital', 
         'Cuba Memorial Hospital Inc', 'Memorial Hosp of Wm F & Gertrude F Jones A/K/A Jones Memorial Hosp', 
         'United Health Services Hospitals Inc. - Binghamton General Hospital', 'Our Lady of Lourdes Memorial Hospital Inc', 
         'United Health Services Hospitals Inc. - Wilson Medical Center', 'Olean General Hospital', 
         'TLC Health Network Tri-County Memorial Hospital', 'Auburn Memorial Hospital', 'Brooks Memorial Hospital', 
         "Woman's Christian Association", 'Westfield Memorial Hospital Inc', 'TLC Health Network Lake Shore Hospital', 
         'Arnot Ogden Medical Center', 'St Josephs Hospital', 'Chenango Memorial Hospital Inc', 
         'Champlain Valley Physicians Hospital Medical Center', 'Columbia Memorial Hospital', 
         'Cortland Regional Medical Center Inc', "O'Connor Hospital", 'Margaretville Hospital', 
         'Delaware Valley Hospital Inc', 'St Francis Hospital', 'Vassar Brothers Medical Center', 
         'Northern Dutchess Hospital', 'Buffalo General Hospital', "Women And Children's Hospital Of Buffalo", 
         'Erie County Medical Center', 'Mercy Hospital', 'Millard Fillmore Hospital', 'Roswell Park Cancer Institute', 
         'Sisters of Charity Hospital', 'University Hospital', 'Kenmore Mercy Hospital', 'Bertrand Chaffee Hospital', 
         'Sisters of Charity Hospital - St Joseph Campus', 'Elizabethtown Community Hospital', 'Moses-Ludington Hospital', 
         'Adirondack Medical Center-Saranac Lake Site', 'Alice Hyde Medical Center', 'Nathan Littauer Hospital', 
         'United Memorial Medical Center North Street Campus', 'Little Falls Hospital', 'Samaritan Medical Center', 
         'River Hospital, Inc.', 'Carthage Area Hospital Inc', 'Lewis County General Hospital', 
         'Nicholas H Noyes Memorial Hospital', 'Oneida Healthcare Center', 'Community Memorial Hospital Inc', 
         'Highland Hospital', 'Rochester General Hospital', 'Strong Memorial Hospital', 'Monroe Community Hospital', 
         'Lakeside Memorial Hospital', 'The Unity Hospital of Rochester', "St. Mary's Healthcare", 'Glen Cove Hospital', 
         'Long Beach Medical Center', 'Winthrop-University Hospital', 'Mercy Medical Center', 'Franklin Hospital', 
         'South Nassau Communities Hospital', 'Nassau University Medical Center', 'North Shore University Hospital', 
         'Syosset Hospital', 'St. Joseph Hospital', 'Plainview Hospital', 'Eastern Niagara Hospital - Lockport Division', 
         'Niagara Falls Memorial Medical Center', 'Degraff Memorial Hospital', 'Mount St Marys Hospital and Health Center', 
         'Eastern Niagara Hospital - Newfane Division', 'Rome Memorial Hospital, Inc', 'St Elizabeth Medical Center', 
         'Faxton-St Lukes Healthcare St Lukes Division', 'UPSTATE University Hospital at Community General', 
         'St Josephs Hospital Health Center', 'University Hospital SUNY Health Science Center', 'Crouse Hospital', 
         'Geneva General Hospital', 'Clifton Springs Hospital and Clinic', 'F F Thompson Hospital', 
         'Orange Regional Medical Center-Middletown Campus', "St Luke's Cornwall Hospital/Newburgh", 
         "St. Luke's Cornwall Hospital/Cornwall", 'Orange Regional Medical Center-Goshen Campus', 
         'St Anthony Community Hospital', 'Bon Secours Community Hospital', 'Medina Memorial Hospital', 'Oswego Hospital', 
         'Aurelia Osborn Fox Memorial Hospital', 'Mary Imogene Bassett Hospital', 'Putnam Hospital Center', 
         "Seton Health System-St Mary's Campus", 'Samaritan Hospital', 'Helen Hayes Hospital', 'Nyack Hospital', 
         'Good Samaritan Hospital of Suffern', 'Summit Park Hospital-Rockland County Infirmary', 'Claxton-Hepburn Medical Center', 
         'Massena Memorial Hospital', 'Edward John Noble Hospital of Gouverneur', 'Canton-Potsdam Hospital', 
         'Clifton-Fine Hospital', 'Saratoga Hospital', 'Ellis Hospital', "Ellis Hospital - Bellevue Woman's Care Center Division", 
         'Cobleskill Regional Hospital', 'Schuyler Hospital', 'Corning Hospital', 'St James Mercy Hospital', 
         'Ira Davenport Memorial Hospital Inc', 'Brookhaven Memorial Hospital Medical Center Inc', 'Southampton Hospital', 
         'Eastern Long Island Hospital', 'John T Mather Memorial Hospital of Port Jefferson New York Inc', 'St Charles Hospital', 
         'Huntington Hospital', 'Southside Hospital', 'Good Samaritan Hospital Medical Center', 'Peconic Bay Medical Center', 
         'St Catherine of Siena Hospital', 'Catskill Regional Medical Center - G. Hermann Site', 'Catskill Regional Medical Center', 
         'Cayuga Medical Center at Ithaca', 'Benedictine Hospital', 'Kingston Hospital', 'Ulster County Area Medical Services', 
         'Brooklyn Hospital Center', 'Elmhurst Hospital Center', 'Kingsbrook Jewish Medical Center', 'Interfaith Medical Center', 
         'Woodhull Medical and Mental Health Center', 'Lincoln Medical and Mental Health Center', 'Metropolitan Hospital Center', 
         'NYC Health + Hospitals/Gotham Health/Harlem', 'NYC Health + Hospitals/Coler-Goldwater Specialty Hospital', 
         'NYC Health + Hospitals/Coney Island', 'NYC Health + Hospitals/Jacobi', 'NYC Health + Hospitals/Lincoln', 
         'NYC Health + Hospitals/Bellevue', 'NYC Health + Hospitals/Elmhurst', 'NYC Health + Hospitals/Kings County', 
         'NYC Health + Hospitals/Harlem', 'NYC Health + Hospitals/Queens', 'NYC Health + Hospitals/Correctional Health Services', 
         'NYC Health + Hospitals/North Central Bronx', 'NYC Health + Hospitals/Metropolitan', 'NYC Health + Hospitals/Jacobi Medical Center', 
         'NYC Health + Hospitals/Lincoln Medical Center', 'NYC Health + Hospitals/Harlem Hospital Center', 'NYC Health + Hospitals/Queens Hospital Center', 
         'NYC Health + Hospitals/Bellevue Hospital Center', 'NYC Health + Hospitals/Gotham Health/St. George', 'NYC Health + Hospitals/Correctional Health Services', 
         'NYC Health + Hospitals/Bellevue Hospital Center/Behavioral Health', 'NYC Health + Hospitals/North Central Bronx Hospital', 'NYC Health + Hospitals/Coney Island Hospital', 
         'NYC Health + Hospitals/Correctional Health Services - Anna M. Kross Center', 'NYC Health + Hospitals/Correctional Health Services - Rikers Island', 
         'NYC Health + Hospitals/Correctional Health Services - Rose M. Singer Center', 'NYC Health + Hospitals/Correctional Health Services - George R. Vierno Center', 
         'NYC Health + Hospitals/Correctional Health Services - Robert N. Davoren Center', 'NYC Health + Hospitals/Correctional Health Services - Otis Bantum Correctional Center', 
         'NYC Health + Hospitals/Correctional Health Services - James A. Farley Center', 'NYC Health + Hospitals/Correctional Health Services - North Infirmary Command', 
         'NYC Health + Hospitals/Correctional Health Services - South Infirmary Command', 'NYC Health + Hospitals/Correctional Health Services - North Infirmary Command', 
         'NYC Health + Hospitals/Correctional Health Services - South Infirmary Command', 'NYC Health + Hospitals/Correctional Health Services - East River Academy', 
         'NYC Health + Hospitals/Correctional Health Services - Midwood Medical Unit', 'NYC Health + Hospitals/Correctional Health Services - Rikers Island Medical Unit', 
         'NYC Health + Hospitals/Correctional Health Services - West Facility Medical Unit'])

    age_group = st.selectbox('Age Group', 
         ['','70 or Older', '18 to 29', '0 to 17', '30 to 49', '50 to 69'])

    zip_code = st.selectbox('Zip Code', 
         ['',105, 109, 112, 120, 121, 122, 123, 124, 125, 127, 128, 129, 133, 134, 137, 138, 114, 130, 101, 145, 147, 
         148, 139, 117, 136, 146, 140, 141, 142, 131, 144, 100, 115, 149, 110, 104, 126, 107, 143, 132, 135, 111, 
         113, 119, 116, 118, 103, 108, 106])

    gender = st.selectbox('Gender', ['','F', 'M', 'U'])

    race = st.selectbox('Race', 
         ['','White', 'Other Race', 'Black/African American', 'Unknown', 'Multi-racial'])

    ethnicity = st.selectbox('Ethnicity', 
         ['','Not Span/Hispanic', 'Spanish/Hispanic', 'Unknown', 'Multi-ethnic'])

    length_of_stay = st.selectbox('Length of Stay', 
         ['',6, 3, 2, 5, 9, 1, 20, 4, 37, 8, 27, 21, 23, 7, 31, 14, 11, 46, 18, 28, 10, 15, 17, 32, 13, 24, 22, 
         12, 33, 19, 16, 34, 26, 58, 39, 40, 29, 25, 38, 35, 100, 30, 72, 36, 110, 96, 63, 43, 44, 75, 57, 42, 
         115, 87, 73, 69, 59, 76, 81, 86, 52, 118, 78, 88, 54, 47, 61, 66, 94, 41, 45, 112, 82, 64, 77, 60, 
         53, 56, 49, 98, 70, 97, 90, 51, 62, 50, 65, 84, 89, 55, 48, 71, 92, 79, 109, 80, 83, 67, 111, 95, 
         91, 68, 74, 101, 117, 85, 103, 104, 102, 108, 114, 106, 107, 116, 113, 119, 93, 105, 99, 130])

    type_of_admission = st.selectbox('Type of Admission', 
         ['','Emergency', 'Urgent', 'Elective', 'Not Available', 'Newborn', 'Trauma'])

    patient_disposition = st.selectbox('Patient Disposition', 
         ['','Skilled Nursing Home', 'Inpatient Rehabilitation Facility', 'Home or Self Care', 'Home w/ Home Health Services', 
         'Short-term Hospital', 'Left Against Medical Advice', 'Expired', 'Facility w/ Custodial/Supportive Care', 
         'Hospice - Home', 'Hospice - Medical Facility', 'Psychiatric Hospital or Unit of Hosp', 'Court/Law Enforcement', 
         'Hosp Basd Medicare Approved Swing Bed', 'Federal Health Care Facility', "Cancer Center or Children's Hospital", 
         'Another Type Not Listed', 'Medicaid Cert Nursing Facility', 'Medicare Cert Long Term Care Hospital', 
         'Critical Access Hospital'])

    ccs_diagnosis_code = ccs_diagnosis_code = st.selectbox(
         'CSS Diagnosis Code',
         ['',122])
    ccs_diagnosis_description =  st.selectbox(
         'CSS Diagnosis Description',
         ['','Pneumonia', 'Pneumonia (except that caused by tuberculosis or sexually transmitted disease)'])
    ccs_procedure_code =  st.selectbox(
         'CSS Procedure Code',
         ['',0., 216., 54., 39., 217., 223., 222., 37., 174., 191., 34., 173., 58., 38., 146., 188., 65., 35., 93., 45., 231., 4., 41., 42., 110., 198., 57., 175., 219., 61., 95., 71., 63., 33., 48., 47., 155., 70., 98., 76., 36., 40., 213., 215., 90., 193., 163., 228., 227., 100., 221., 208., 225., 169., 202., 108., 157., 78., 211., 88., 168., 107., 73., 27., 229., 101., 111., 205., 89., 214., 171., 97., 81., 102., 178., 196., 197., 179., 177., 195., 31., 69., 185., 199., 201., 86., 192., 226., 161., 170., 153., 91., 154., 224., 49., 99., 84., 67., 85., 82., 96., 203., 55., 159., 83., 113., 112., 30., 29., 209., 109., 207., 130., 11., 183., 180., 75., 5., 26., 103., 3., 115., 147., 8., 94., 162., 62., 23., 92., 206., 142., 160., 210., 204., 118., 165., 60., 172., 128., 19., 10., 80., 145., 194., 44., 156., 32., 164., 148., 50., 117., 131., 212., 77., 52., 218., 187., 1., 7., 28., 43., 9., 64., 66., 186., 25., 119., 116., 59., 166., 181., 51., 87., 2., 104., 132., 79., 72., 189., 12., 53., 176., 190., 150., 16., 139., 152., 74., 167., 124., 144., 220., 158., 151., 137., 6., 200., 182., 999.]
         )
    ccs_procedure_description = st.selectbox(
         'CSS Procedure Description',
         ['','NO PROC', 'RESP INTUB/MECH VENTIL', 'OT VASC CATH; NOT HEART',
         'INCISION OF PLEURA', 'OTHER RESP THERAPY',
         'ENTERAL/PARENTERAL NUTR', 'BLOOD TRANSFUSION',
         'DX BRONCHOSCOPY & BIOPS', 'OT NON-OR THER PRC SKIN',
         'ARTERIO/VENOGRAM-NOT HH', 'TRACHEOSTOMY; TEMP/PERM',
         'OT DX PRC SKIN/SUBCUTAN', 'HEMODIALYSIS', 'OT DX PRCS ON LUNG',
         'TRTMNT,FRAC HIP/FEMUR', 'CEREBRAL ARTERIOGRAM',
         'BONE MARROW BIOPSY', 'TRACHE-/LARYNG-OSCOPY',
         'OT NON-OR UP GI THER PR', 'PERC TRANSLUM COR ANGIO',
         'OTHER THERAPEUTIC PRCS', 'DIAGNOSTIC SPINAL TAP',
         'OT NON-OR THER PRC RESP', 'OT OR RX PRCS RESP SYS',
         'OT DX PRCS URINARY TRCT', 'MAG RESONANCE IMAGING',
         'ARTERIOVENOUS FISTULA', 'OT OR THER PRC SKN/BRST',
         'ALCO/DRUG REHAB/DETOX', 'OT OR PRCS VES NOT HEAD',
         'OT NON-OR LW GI THER PR', 'GASTROSTOMY; TEMP/PERM',
         'OT NON-OR THER CARDIO', 'OTHER OR THER PRCS NOSE',
         'CARDIAC PACEMAKER/DEFIB', 'DX CARDIAC CATHETERIZTN',
         'ARTHROCENTESIS', 'UP GASTRO ENDOSC/BIOPSY',
         'OT NON-OR GI THER PRCS', 'COLONOSCOPY AND BIOPSY',
         'LOBECTOMY/PNEUMONECTOMY', 'OT DX PRCS OF RESP TRCT',
         'PHYS THER EXER, MANIPUL', 'OT PHYS THER/REHAB',
         'EXCISION; LYS PERI ADHS', 'DX ULTRASOUND HEART',
         'OT NON-OR THER PRC MUSC', 'PROPHYLACTIC VAC/INOCUL',
         'OT DX PRC (INTERVW,EVAL', 'ENDOSCOPY URINARY TRACT',
         'NASOGASTRIC TUBE', 'RADIOISOTOPE PULM SCAN',
         'CONV OF CARDIAC RHYTHM', 'DEBRIDE WOUND,INF,BURN',
         'ELECTROCARDIOGRAM', 'INDWELLING CATHETER',
         'AMPUTATE LOWER EXTRMITY', 'COLORECTAL RESECTION',
         'THERAPEUTIC RADIOLOGY', 'ABDOMINAL PARACENTESIS',
         'INCIS/DRAIN, SKIN/SUBCU', 'EXTRACORP LTIHO;URINARY',
         'ILEO- & OT ENTER-OSTOMY', 'CONTROL OF EPISTAXIS',
         'NONOP RMVL FOREIGN BODY', 'TRANSURETHRAL EXCISION',
         'OT NON-OR THER PRC URIN', 'ARTERIAL BLOOD GASES',
         'EXPLORATORY LAPAROTOMY', 'TRACTN, SPLNT, OT WOUND',
         'SUTURE SKIN/SUBCUT TISS', 'OTHER GI DX PRCS', 'HEMORRHOID PRCS',
         'URETERAL CATHETERIZATN', 'CT SCAN CHEST',
         'DX ULTRASOUND AB/RETRO', 'OTHER DX ULTRASOUND', 'CT SCAN ABDOMEN',
         'COMP AXIAL TOMOGR (CT)', 'DX ULTRASOUND URINARY',
         'DX PRCS ON NOSE & MOUTH', 'ESOPHAGEAL DILATATION',
         'UPPER GI X-RAY', 'ELECTROENCEPHALOGRAM', 'CARDIAC STRESS TESTS',
         'OTHER HERNIA REPAIR', 'DX ULTRASOUND HEAD/NECK',
         'OT DX RADIO & RELATED', 'OT OR THER PRCS ON BONE',
         'EXCISION OF SKIN LESION', 'HIP REPLACEMENT,TOT/PRT',
         'PERITONEAL DIALYSIS', 'ARTHROPLASTY-NOT HIP/KN',
         'CANCER CHEMOTHERAPY', 'OTHER OR HEART PRCS', 'OT OR GI THER PRCS',
         'CHOLECYSTECTOMY/EXPLOR', 'OT THER PRCS; HEM/LYMPH',
         'INGUINAL/FEMORAL HERNIA', 'ENDO RETRO CAN OF PANCR',
         'OT OR LOW GI THER PRCS', 'ELECTROGR CARDIAC MONIT',
         'PERIPH VASCULAR BYPASS', 'OT DX PRCS ON MUSC/SKEL',
         'BIOPSY OF LIVER', 'TRANS RES PROSTATE-TURP',
         'OT OR THER PRCS URINARY', 'TONSIL-/ADENOID-ECTOMY',
         'ORAL AND DENTAL SVCS', 'RADIOISOTOPE SCAN/FUNCT',
         'PRCS ON THE URETHRA', 'RADIOISOTOPE BONE SCAN',
         'OT DX PRCS; FEMALE ORGN', 'DX ENDOCRINE PRCS',
         'ROUTINE CHEST X-RAY', 'OTHER CT SCAN', 'SMALL BOWEL RESECTON',
         'INS CATHETER/SPNL STIM', 'OT THERAPEUTIC EAR PRCS',
         'NEPHRO-/NEPHROS-TOMY', 'LAMINECTOMY; EXC IV DSC', 'CIRCUMCISION',
         'TRTMNT,FRAC LOWR EXTREM', 'OT NON-OR THER NERV SYS',
         'OT OR UP GI THER PRCS', 'OT OR THER PRC ON JOINT',
         'OT DX CARDIOVASC PRCS', 'MYRINGOTOMY', 'OTHER BOWEL DX PRCS',
         'MICRO EX (BACT SMEAR)', 'PARTIAL EXCISION BONE',
         'OT THER PRCS ON MUSCLES', 'OTHER RADIOISOTOPE SCAN',
         'SWAN-GANZ CATH MONITOR', 'OT OR THER PRCS; MALE',
         'BREAST BIOPSY & DX PRCS', 'EMBOL-/ENDARTER-ECTOMY', 'SKIN GRAFT',
         'DX DILAT/CURETTAGE -D&C', 'OT THER PRCS EYELIDS',
         'THYROIDECTOMY;PART/FULL', 'APPENDECTOMY',
         'TRTMNT,FRAC RADIUS/ULNA', 'DX ULTRASOUND OF GI',
         'COR ARTERY BYP GRF-CABG', 'INJ/ASP MUSC,TENDONS,ST',
         'OT NON-OR THER PRC NOSE', 'OT OR THER PRC MUSC/SKL',
         'OT FRACTURE/DISLOC PRC', 'EXTRA CIRC AUX OPEN HRT',
         'OT NON-OR THER PRCS; M', 'OT NON-OR THER PRC; FEM',
         'DX PHYSICAL THERAPY', 'PROCTOSCOPY & AR BIOPSY',
         'AORTIC RESECTION; REPL', 'PSYCHO/PSYCHI EVAL/THER',
         'INTRAVENOUS PYELOGRAM', 'INCISION & EXCISION CNS',
         'OTHER DX NERV SYS PRCS', 'PLASTIC PRCS ON NOSE',
         'HEART VALVE PRCS', 'OTHER OR THER NERV SYS',
         'BONE MARROW TRANSPLANT', 'PRCS ON SPLEEN', 'LOWER GI X-RAY',
         'DX PRCS ON EAR', 'OOPHORECTOMY; UNI/BILAT',
         'DX PRCS; MALE GENITAL', 'OT OR PRCS ON VES HEAD',
         'LUMPECTOMY, QUAD BREAST', 'MYELOGRAM', 'ENDARTERECTOMY;VES HEAD',
         'LAPAROSCOPY', 'IRR XCRANIAL VENT SHUNT',
         'NEPHRECTOMY; PART/TOTAL', 'OT OR THER PRC; FEM ORG',
         'LOC EXC LRG INTEST LESN', 'COLOSTOMY; TEMP/PERM',
         'CONTRAST AORTOGRAM', 'OT THER ENDOCRINE PRCS',
         'VARI VEIN STRIP;LOW LMB', 'OT ORGAN TRANSPLANTATN',
         'ARTERIO FEMORAL/LOW ART', 'DIV OF JOINT CAPSULE',
         'REPAIR RETINAL TEAR', 'FETAL MONITORING', 'ARTHROPLASTY KNEE',
         'GASTRECTOMY; PART/TOTAL', 'MASTECTOMY', 'HYSTERECTOMY; AB/VAG',
         'TRTMNT,FACE FRACT/DISLC', 'OPHTHALM-/OT-OLOGIC DX',
         'SPINAL FUSION', 'EXC OF SEMI CART KNEE',
         'OT PRCS TO ASSIST DELIV', 'DECOMP PERIPHERAL NERVE',
         'NONOP URINARY SYS MEASR', 'MAMMOGRAPHY', 'UNGROUPABLE'])

    apr_drg_code = st.selectbox(
      'APR DRG Code',
         ['',137, 139, 130, 131, 121, 5, 950, 138, 132, 894, 951, 120, 892, 890, 710, 952, 4, 893, 622, 3, 724, 634, 2, 1, 580]
          )
    apr_drg_description = st.text_input('APR DRG Description', '')
    apr_mdc_code = st.selectbox(
     'APR MDC Code',
      ['',4, 24, 18, 15])
    apr_mdc_description = st.selectbox(
      'APR MDC Description',
         ['','Diseases and Disorders of the Respiratory System',
         'Human Immunodeficiency Virus Infections',
         'Infectious and Parasitic Diseases, Systemic or Unspecified Sites',
         'Newborns and Other Neonates with Conditions Originating in the Perinatal Period'])
    apr_severity_of_illness_code = st.selectbox(
       'APR Severity of Illness Code',
         ['',3, 1, 2, 4])
    apr_severity_of_illness_description = st.selectbox(
       'APR Severity of Illness Description',
         ['','Major', 'Minor', 'Moderate', 'Extreme'])
    apr_medical_surgical_description = st.selectbox(
       'APR Medical Surgical Description',
         ['','Major', 'Minor', 'Moderate', 'Extreme'])
    payment_typology_1 = st.selectbox(
       'Payment Typology 1',
         ['','unknown', 'Blue Cross/Blue Shield', 'Medicare', 'Medicaid',
         'Private Health Insurance', 'Self-Pay', 'Federal/State/Local/VA',
         'Miscellaneous/Other', 'Department of Corrections',
         'Managed Care, Unspecified', 'Unknown'])
    
    # Collect other inputs similarly...

    if st.button("Predict"):
        data = [health_service_area, hospital_county, facility_name, age_group, zip_code, gender, race, ethnicity,
              length_of_stay, type_of_admission, patient_disposition, ccs_diagnosis_code, ccs_diagnosis_description,
              ccs_procedure_code, ccs_procedure_description, apr_drg_code, apr_drg_description, apr_mdc_code,
              apr_mdc_description, apr_severity_of_illness_code, apr_severity_of_illness_description,
              apr_medical_surgical_description, payment_typology_1]
        
        # Preprocess input data
        X_scaled = preprocess_input(data)
        
        # Make prediction
        prediction = model.predict(X_scaled)
        
        st.write(f"The patient is classified as {labels[np.argmax(prediction)]} risk for mortality from pneumonia.")

# Power BI Dashboard Page Content
elif st.session_state.page == "Dashboard":
    st.title("Dashboard")
    st.markdown("View the interactive dashboard below.")
    
    # Load the Power BI dashboard
    load_dashboard()
