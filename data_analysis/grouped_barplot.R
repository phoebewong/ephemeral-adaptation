# Data
library(tidyverse)
setwd("~/Documents/ephemeral-adaptation/data_analysis")
time_df = read.csv("time_data.csv", stringsAsFactors = FALSE)

sd(time_df[condition == 'control', ])

time_df %>% 
  add_count(condition, correctly_predicted) %>% 
  group_by(condition, correctly_predicted) %>% 
  dplyr::summarize(Median = median(selection_time), SE = sd(selection_time)/unique(n), count = unique(n)) %>% 
  # mutate()
  # add_count(condition, correctly_predicted) %>% 
  ggplot(., aes(x = correctly_predicted, y = Median, fill = condition)) +
  geom_bar(stat="identity", position='dodge') +
  geom_errorbar(aes(ymin = Median - SE, ymax = Median + SE), width = 0.2, position = position_dodge(0.9)) +
  theme_minimal()


wilcox.test(time_df$selection_time[time_df$correctly_predicted == 'True' & time_df$condition == 'control'], 
            time_df$selection_time[time_df$correctly_predicted == 'False' & time_df$condition == 'control'], 
            alternative = "two.sided", exact = FALSE, conf.int = TRUE, conf.level = .95)

# ANOVA
fit <- aov(selection_time~as.factor(condition) * as.factor(menu_order), data = time_df)
summary(fit)


# ANOVA
fit2 <- aov(selection_time~as.factor(condition) * as.factor(correctly_predicted), data = time_df)
summary(fit2)

f1 <- function(x) sum(x=='yes')

mydata %>% 
  group_by(group) %>% 
  summarise_each(funs(f1), var1:var5) %>% 
  gather(Var, Val, var1:var5)%>%
  ggplot(., aes(x=Var, y=Val, fill=group))+
  geom_bar(stat="identity", position='dodge')