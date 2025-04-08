T=readtable("附件1：物流网络历史货量数据.xlsx","VariableNamingRule","preserve");
x=T(strcmp(T.("场地1"),"DC14"),:);
y=x(strcmp(x.("场地2"),"DC10"),:);
bar(y.("货量"));
set(gca,"YScale","log");