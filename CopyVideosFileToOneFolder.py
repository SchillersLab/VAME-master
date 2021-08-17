import glob
from shutil import copyfile

def main():
    videosFileLocation = r'C:\Users\Jackie.MEDICINE\Desktop\VAME-master\new_vi\10_1_17_new_JAABA\*\movie_comb*.avi'
    outputfolder = r'C:\Users\Jackie.MEDICINE\Desktop\VAME-master\new_vi\AllTogether'
    experimant_name = 'EPC_M26_2017-10-01_'
    formatV = 'avi'
    videosList = glob.glob(videosFileLocation)

    counter = 1
    for i in videosList:
        d = '%s/%s%03d.%s' % (outputfolder, experimant_name, counter, formatV)
        copyfile(i, d)
        counter += 1


if __name__ == "__main__":
    main()
