# rgeomex-py, data-raw/01_export_from_r.R
# Export the rgeomex (R) datasets to GeoPackage (sf objects) and CSV (tables),
# with all text converted to UTF-8. The Python script 02_build_parquet.py then
# splits the large datasets by state and writes the GeoParquet files.
#
# Run in R (Mac), with rgeomex installed:
#   source("data-raw/01_export_from_r.R")

out <- "data-raw/rgeomex_export"
dir.create(out, showWarnings = FALSE, recursive = TRUE)

# text Latin-1 -> UTF-8 (only the values that are not valid UTF-8)
a_utf8 <- function(x){
    for(v in names(x)){
        col <- x[[v]]
        if(is.factor(col)) col <- as.character(col)
        if(is.character(col)){
            bad <- !is.na(col) & !validUTF8(col)
            col[bad] <- iconv(col[bad], from = "latin1", to = "UTF-8")
            col <- enc2utf8(col)
            x[[v]] <- col
        }
    }
    x
}

# repair sf objects whose geometry column or CRS is not well defined (e.g. hrl_mx)
repara_sf <- function(x, nombre){
    geo <- names(x)[vapply(x, inherits, logical(1), what = "sfc")]
    if(length(geo) == 0) stop(nombre, ": no geometry column")
    x <- sf::st_set_geometry(as.data.frame(x), geo[1])
    if(is.na(sf::st_crs(x))){
        bb <- sf::st_bbox(x)
        if(bb["xmin"] >= -180 && bb["xmax"] <= 180 && bb["ymin"] >= -90 && bb["ymax"] <= 90){
            sf::st_crs(x) <- 4326
            message(nombre, ": CRS missing; set to EPSG:4326 (coordinates are lon/lat)")
        } else {
            warning(nombre, ": CRS missing and coordinates are not lon/lat; check it")
        }
    }
    x
}

items <- sub(" .*", "", data(package = "rgeomex")$results[, "Item"])
resumen <- list()
for(i in items){
    e <- new.env()
    data(list = i, package = "rgeomex", envir = e)
    x <- get(i, envir = e)
    if(inherits(x, "sf")){
        x <- repara_sf(x, i)
        x <- a_utf8(x)
        f <- file.path(out, paste0(i, ".gpkg"))
        sf::st_write(x, f, layer = i, delete_dsn = TRUE, quiet = TRUE)
        tipo <- "sf"; crs <- as.character(sf::st_crs(x)$epsg)
    } else {
        x <- a_utf8(as.data.frame(x))
        f <- file.path(out, paste0(i, ".csv"))
        data.table::fwrite(x, f)                       # UTF-8, keeps leading zeros as text
        tipo <- "table"; crs <- NA_character_
    }
    resumen[[i]] <- data.frame(dataset = i, tipo = tipo, filas = nrow(x),
                               crs = crs, mb = round(file.size(f) / 1e6, 1))
    message(i, " -> ", basename(f))
}
resumen <- do.call(rbind, resumen)
data.table::fwrite(resumen, file.path(out, "export_summary.csv"))
print(resumen)
