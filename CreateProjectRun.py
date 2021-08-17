import vame
import glob
from shutil import copyfile

# can be used also for csv copys
def change_video_names():
    # csv
   
    videosFileLocation = r'\\192.114.20.177\f\videos\vi_amir\vi_withoutHighTable\*.csv' # change
    outputfolder = r'I:\VAME_projects\minmax_LowerBach_Rightcam-Mar16-2021' # change
    #experimant_name = 'EPC_M26_2017-09-28_'
    formatV = 'csv'
    videosList = glob.glob(videosFileLocation)

    counter = 1
    for i in videosList:
        #file_name = (i.split('\\'))[-2]
        temp_file_name = (i.split('DLC'))[0]
        file_name = (temp_file_name.split('\\'))[-1]
        d = '%s/%s.%s' % (outputfolder, file_name, formatV)
        copyfile(i, d)
        counter += 1

    #video
    videosFileLocation = r'' # change
    outputfolder = r'C:\Users\Jackie.MEDICINE\Desktop\VAME-master\vi_succsess' # change
    #experimant_name = 'EPC_M26_2017-09-28_'
    formatV = 'avi'
    videosList = glob.glob(videosFileLocation)

    counter = 1
    for i in videosList:
        file_name = (i.split('\\'))[-2]
        d = '%s/%s.%s' % (outputfolder, file_name, formatV)
        copyfile(i, d)
        counter += 1




if __name__ == "__main__":
    projectName = 'AMIR_plan1'
    workingDirectory = 'D:\AMIR_vame_projects'
    experimant_name = 'Reach_6_08'
    #formatV = 'avi'
    #change_video_names()
    #videosList_raw = r'C:\Users\Jackie.MEDICINE\Desktop\VAME-master\new_vi\*\*\movie_comb.avi'
    
    #videosFileLocation = r'C:\Users\Jackie.MEDICINE\Desktop\VAME-master\vi\%s*.%s' % (experimant_name, formatV)
    videosFileLocation = r'\\192.114.20.177\f\Amir_data_VAME_allAnimals\ALL_by_name'

    videosList = glob.glob(videosFileLocation)

    config = vame.init_new_project(project=projectName,
                                   videos=videosList,
                                   working_directory=workingDirectory, videotype='.mp4')
