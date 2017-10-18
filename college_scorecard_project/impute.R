# loading library
library(mice)

# reading in data
df <- read.csv(file="df_college3.csv", header=TRUE, sep=",", stringsAsFactors = FALSE)

# we dont need the UNITID
df <- df[,-1]

# Convert Privacy Suppressed instances to NA
df[df=="PrivacySuppressed"]<-NA

# define a function that convert columns to appropriate data type 
categorical = c('PREDDEG','HIGHDEG','CONTROL','REGION','ICLEVEL')

convertType <- function(df, categorical){
  for(name in names(df)){
    if(grepl('ISNULL', name) || 
       !is.na(match(name, categorical)) || 
       (grepl('CIP', name) & !grepl('PCIP', name))){
        df[name] <- as.factor(df[[name]])
      } else {
        df[name] <- sapply(df[name], as.numeric)
      }
    }
  return(df)
}

df <- convertType(df, categorical)

# Impute  using CART
imputed3de <- mice(df, m = 2, maxit = 1, method = 'cart', seed = 1111)

# write to csv
write.csv(complete(imputed3de, action = 'long', inc =TRUE), "imputed3de.csv")
