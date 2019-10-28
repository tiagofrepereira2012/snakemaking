patient_gene_mutations = {
  "patientA": ["RCOR1", "TP53", "KRAS"],
  "patientB": ["NCOR1", "CDKN2A", "B2M"]
}

rule all:
    input:
        "patient_data/patientA_output.tsv",
        "patient_data/patientB_output.tsv"

rule get_mutation_file:
    output:
        "mutation_data/{gene_id}_output.tsv"
    shell:
        """
        touch {output}
        """

rule get_patient_output:
    input:
        lambda wildcards: \
            ["mutation_data/{0}_output.tsv".format(gene_id) \
                for gene_id in patient_gene_mutations[wildcards.patient_id]
            ]
    output:
        "patient_data/{patient_id}_output.tsv"
    shell:
        """
        touch {output}
        """

