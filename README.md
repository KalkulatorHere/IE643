For a brief report and introduction of the task visit [Go to report](report.md)

There are several folders added each having a short description for tasks.

There are two branches and preprocessing branch contains preprocessing code for im2latex-100k 

I have already provided all dataset links and preprocessed ready to use CROHME dataset

You can access model in its final state in model folder

Download that model and you can run inferences straightaway using snippets in CROHME.ipynb and gradio.

If you want to train model from scratch use following method: use finetune_im2latex.ipynb to finetune on im2latex, you will generate a model, further finetune that model with CROHME data using CROHME.ipynb code to generate good results on handwritten mathematical equations

Alternatively, you can use finetuning-on-hf.ipynb with Alfrauch dataset for 1st finetune stage

Similar method can be used to finetune on IAM dataset and CTW-1500 as well

