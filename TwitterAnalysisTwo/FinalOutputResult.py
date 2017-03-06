import codecs
class FinalOutputResult:
    @staticmethod
    def set_final_output(celebrity, final_conclusion, file_name):
        name_array = []
        celebrityimage_array = []
        profession_array = []
        bestwork_array = []
        analysisresult_array = []
    
        name_array.append(celebrity.get_name().strip().strip('\n'))
        profession_array.append(celebrity.get_profession().strip().strip('\n'))
        bestwork_array.append(celebrity.get_best_work().strip().strip('\n'))
        celebrityimage_array.append(celebrity.get_image_link().strip().strip('\n'))
        analysisresult_array.append(final_conclusion)
        outfile = codecs.open(file_name, 'a', "utf-8")
        output = zip(name_array, analysisresult_array,profession_array, bestwork_array, celebrityimage_array)
    
        for line in output:
            linecontent = ', '.join(line)
            print(linecontent) # print the result to the console
            outfile.write(linecontent + '\n')
        outfile.close()  