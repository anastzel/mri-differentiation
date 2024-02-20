import pydicom as dicom
import os

def find_type_from_dicom_with_times(file_path):
    
    try:
        image = dicom.dcmread(file_path)
        try:
            series_description = image.SeriesDescription
        except Exception as e:
            print("SeriesDescription tag doesn't exist. Calculating the image type using the acquisition parameters.")
            
            try:
                echo_time = image.EchoTime
                repetition_time = image.RepetitionTime
                flip_angle = image.FlipAngle
            except Exception as e:
                print(e)
                return None

            if repetition_time < 800 and echo_time < 30 and flip_angle==90:
                return "t1"
            elif repetition_time < 1000 and echo_time < 30 and flip_angle==90:
                return "pd"
            elif repetition_time > 2000 and echo_time > 80 and flip_angle==90:
                return "t2"
            elif repetition_time > 2000 and echo_time > 60 and flip_angle==90:
                return "fse_t2"
            elif echo_time < 30 and flip_angle >= 70 and flip_angle <= 110:
                return "gre_t1"
            elif echo_time < 30 and flip_angle >= 5 and flip_angle <= 20:
                return "gre_t2"
                
        # If SeriesDescription exists
        image_types = ["t1", "t2", "diff"]
        for image_type in image_types:
            if image_type in series_description.lower():
                return series_description
        
        return series_description
    except Exception as e:
        print(e)

def find_type_from_dicom(serie_path):
    
    dicom_filenames = [os.path.join(serie_path, filename) for filename in os.listdir(serie_path) if filename.endswith(".dcm")]
    file_path = dicom_filenames[0]

    try:
        image = dicom.dcmread(file_path)
        try:
            series_description = image.SeriesDescription
        except Exception as e:
            print("SeriesDescription tag doesn't exist. Calculating the image type using the acquisition parameters.")
                
        # If SeriesDescription exists
        if "t2" in series_description.lower():
            return "T2", series_description
        else:
            return "DWI", series_description
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # This works only for IDIBAPS PROSTATE CANCER DATA
    series_path = "/mnt/nfs/incisive2/prostate/idibaps/data/008-000028/008-000028_MR_BL/Series-4"

    type, description = find_type_from_dicom(series_path)
    print(f"MRI Series type: {type}")
    print(f"MRI Series Description: {description}")