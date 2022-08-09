library(tidyverse)
library(ggplot2)
library(plotly)
library(radiant)

setwd('C:\\Users\\Felipe_Demolin\\Documents\\Python\\Quant_B3\\ShinyAPP\\QuantB3')
getwd()

df0 <- read.csv(file = '../../sheets/bovespa_diario_last_date.csv',             # File name or full path of the file
                header = TRUE,        # Whether to read the header or not
                sep = ";",            # Separator of the values
                quote = "\"",         # Quoting character
                dec = "."            # Decimal point
                )          

Ticker = reorder(df0$Stock, -df0$IFR_2)
p <- df0 %>% 
ggplot() +
  aes(x=Ticker, y=df0$IFR_2, fill = df0$IFR_2) +
  geom_bar(stat = "identity")+
  scale_fill_gradient2(low='red', mid='gray', high='darkgreen', midpoint = 50, space='Lab', name="IFR2")+
  geom_hline(yintercept=10, col = 'red', size = 1)+
  geom_hline(yintercept=90, col = 'red', size = 1)+
  geom_text(
    label=format(round(df0$IFR_2, 1), nsmall = 1),
    nudge_x=0, nudge_y=5,
    check_overlap=T, angle = 90,  size=3, color = 'black')+
  xlab("Ticker") + ylab("IFR2")+
  theme(
    axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))


ggplotly(p)


radiant()


