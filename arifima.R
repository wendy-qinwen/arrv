library(ltsa)
library(arfima)
library(forecast)
df=read.table(file = "C:/Users/gaoxc/Desktop/datavix.csv",header=TRUE,sep=",")
# fit <- arfima(df$vix)
# result<- forecast(fit,h = 30)
# forecst_mean <- result[['mean']]

# test_range <- seq(400,1000,1)


# for (v in dff[dff$Date>='2001-06-01',]$Date)
# {
    
# }

result = list()
for (v in df[(df$Date>='2020-03-16')&(df$Date<='2020-07-08'),]$Date)
{

    df_ <- tail(df[df$Date<=v,],170)
    fit <- arfima(df_$log_vix)
	result_<- forecast(fit,h = 30)
	result_v<- append(c(result_[['mean']]),c(v))
	
	write.csv(result_v,paste("C:/Users/gaoxc/Desktop/arfima/",v,"_arfima.txt"))
	result <- append(result,result_v)


}
row<- length(result)
result<-array(result,dim=c(31,row/31))

write.csv(result,"C:/Users/gaoxc/Desktop/riskattitude/data/arfima.txt")