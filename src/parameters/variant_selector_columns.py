def variants_columns(variant_type) -> list:
    """
    TODO
    """
    if variant_type == "SNV-Indel":
        return [
            "variant_key",
            "chrom",
            "pos",
            "id",
            "ref",
            "alt",
            "filter",
            "DP",
            "variant_type",
            "AC",
            "AN",
            "AF",
            "AC_Hom",
            "AC_XX",
            "AN_XX",
            "AF_XX",
            "AC_XY",
            "AN_XY",
            "AF_XY",
            "grpmax",
            "AC_grpmax",
            "AN_grpmax",
            "AF_grpmax",
            "inGnomad",
            "passGnomad",
            "notCoveredByGnomad",
        ]
    else:
        raise TypeError(f"{variant_type} parameters not implemented yet!")
