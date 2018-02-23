(dp1
S'msg_subject'
p2
S'RE: Checkin'
p3
sS'msg_from'
p4
S'Clara Marquardt <cmarquardt@uchicago.edu>'
p5
sS'msg_to'
p6
S'Clara Marquardt <marquardt.clara@gmail.com>'
p7
sS'msg_inbox_outbox'
p8
S'inbox'
p9
sS'msg_id'
p10
V1614943b584edd83
p11
sS'msg_threadid'
p12
V1614943b584edd83
p13
sS'msg_date'
p14
S'Tue, 30 Jan 2018 22:50:27 +0000'
p15
sS'msg_id_mime'
p16
S'<CY1PR11MB07616749FD2505D3BD11C006A7E40@CY1PR11MB0761.namprd11.prod.outlook.com>'
p17
sS'msg_text'
p18
S'Hi Jens, \nMade some progress today in figuring out why I have been running into errors with the updated multi-class version of the codebase. Turns out it is slightly more involved than I had initially thought - I overlooked a few areas that will need to be changed. Two quick things to run by you with regards to how to construct the ensemble. \n1. Each of the individual multi-class learners returns a matrix of dimensions N*number of classes. My plan is to use (number of classes - 1) predictions as features in the ensemble (thus avoiding multi-collinearity). So, instead of the ensemble having one feature per learner it will have (number of classes - 1) features per learner. \n2. In terms of the ensemble learner itself - in the case of an ols learner (our default option), my plan is to construct a multi-class version by constructing a separate model for each class which predicts whether or not the observation belongs to that class (one vs. rest model) (this question is myte in the case of out other ensemble learner - elastic net - for which there exists a multi-class algorithm)\nLet me know if either of these approaches raise any flags with you. Otherwise I will work on implementing these tomorrow. \nI will continue working on this tomorrow. \nClara\n'
p19
sS'msg_reply_to_id_mime'
p20
S'<92F63C365D214C4B8094C19DE4C3E13E24CED252@ssa35.ssa.ad.uchicago.edu>'
p21
sS'msg_label'
p22
(lp23
VIMPORTANT
p24
aVCATEGORY_PERSONAL
p25
aVINBOX
p26
asS'msg_cc'
p27
NsS'msg_bcc'
p28
Ns.