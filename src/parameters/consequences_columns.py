def consequence_columns(variant_type) -> list:
    """
    TODO
    """
    if variant_type == "SNV-Indel":
        return [
            "csq_Consequence",
            "csq_IMPACT",
            "csq_SYMBOL",
            "csq_Gene",
            "csq_Feature_type",
            "csq_Feature",
            "csq_BIOTYPE",
            "csq_EXON",
            "csq_INTRON",
            "csq_CDS_position",
            "csq_Amino_acids",
            "csq_Codons",
        ]
    else:
        raise TypeError(f"{variant_type} parameters not implemented yet!")
