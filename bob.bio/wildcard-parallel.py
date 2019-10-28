TRAIN_DATA = ['./parallel-input/a.txt', 'parallel-input/b.txt', 'parallel-input/c.txt']
OUTPUT_DATA = ['parallel-output/a.out', 'parallel-output/b.out', 'parallel-output/c.out']

OUTPUT_DATA2 = ['parallel-output2/a.out', 'parallel-output2/b.out', 'parallel-output2/c.out']

files= dict(zip(OUTPUT_DATA, TRAIN_DATA))
files2= dict(zip(OUTPUT_DATA2, OUTPUT_DATA))


def DO_SOMETHING_AND_SAVE(a, b):
    print("Do %s and %s " % (a, b) )
    os.system("touch %s" % b)

wildcard_constraints:
    x= '|'.join([re.escape(x) for x in OUTPUT_DATA])

wildcard_constraints:
    y= '|'.join([re.escape(y) for y in OUTPUT_DATA2])




rule all_2:
    input:
        expand('{y}', y= OUTPUT_DATA2),


rule MY_RULE2:
    input:
        input_file= lambda wc: files2[wc.y]
    output:
        output_file= '{y}'
    run:        
        DO_SOMETHING_AND_SAVE(input.input_file, output.output_file)





rule all_1:
    input:
        expand('{x}', x= OUTPUT_DATA),

rule MY_RULE:
    input:
        input_file= lambda wc: files[wc.x]
    output:
        output_file= '{x}'
    run:        
        DO_SOMETHING_AND_SAVE(input.input_file, output.output_file)
