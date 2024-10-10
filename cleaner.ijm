a = getArgument;
print(a)
path = split(a)
print(path[0])
print(path[1])
print(path[2])
print(path[3])
imgfilepath = path[0]
foldername = path[1]
name = path[2] + ".tif";
name2 = path[3]
open(imgfilepath);
run("Split Channels");
r = name2+" (red)"
g = name2+" (green)"
b = name2+" (blue)"
selectWindow(r);
selectWindow(g);
selectWindow(b);
run("Images to Stack", "name=Stack title=[] use");
run("BaSiC ", "processing_stack=Stack flat-field=None dark-field=None shading_estimation=[Estimate shading profiles] shading_model=[Estimate both flat-field and dark-field] setting_regularisationparametes=Automatic temporal_drift=[Replace with zero] correction_options=[Compute shading and correct images] lambda_flat=0.50 lambda_dark=0.50");
selectWindow("Flat-field:Stack");
selectWindow("Dark-field:Stack");
selectWindow("Corrected:Stack");
run("Stack to Images");
selectWindow(b);
run("Merge Channels...", "c1=["+r+"] c2=["+g+"] c3=["+b+"] create");
selectWindow("Composite");
run("Stack to RGB");
selectWindow("Composite (RGB)");
//run("Scale...", "x=0.3 y=0.3 interpolation=Bilinear average create");
saveAs("tif", "outputs/" + foldername + "/" + name);
run("Quit")