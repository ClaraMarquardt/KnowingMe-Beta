(dp1
S'msg_subject'
p2
S'Quick multiple outcome related question'
p3
sS'msg_from'
p4
S'Clara Marquardt <marquardt.clara@gmail.com>'
p5
sS'msg_to'
p6
S'Jann Spiess <jann.spiess@gmail.com>'
p7
sS'msg_inbox_outbox'
p8
S'outbox'
p9
sS'msg_id'
p10
V160dd78d87344182
p11
sS'msg_threadid'
p12
V160dd78d87344182
p13
sS'msg_date'
p14
S'Tue, 9 Jan 2018 18:29:29 -0600'
p15
sS'msg_id_mime'
p16
S'<D665A2ED-40B4-4EAB-9B08-3E908EBB6EE3@gmail.com>'
p17
sS'msg_text'
p18
S'Hi Jann,\n \nHope things are going well with the job search!\n \nI was talking to Jens earlier today, and he suggested that I run a method by you. \n \nSome quick context: In the Blattman/CBT paper there are multiple treatment arms (T=control, cash, therapy or cash+therapy). This raises some questions as to how we can adapt our estimation/permutation method. \n \nCurrent idea: Everything stays the same as for a binary treatment but (a) we use a multiclass predictor (e.g. a random forest with a softmax objective) and (b) we calculate a multiclass loss (e.g. overall accuracy across all classes or multiclass log loss). \nAn outline of the algorithm below. \n \n1. Estimate a multiclass classifier\n2. Obtain a multiclass measure of performance\n3. Permute the multiclass outcome the same way we would permute a binary outcome (e.g. shuffling the values within clusters)\n4. Obtain the permuted measure of performance\n5. Repeat steps #3 and #4 n times (n permutations)\n6. Calculate the p-value by comparing the permuted and estimated measures of performance\nDoes this seem like a reasonable approach to you?\n \nMany thanks and best wishes,\nClara'
p19
sS'msg_reply_to_id_mime'
p20
Fnan
sS'msg_label'
p21
(lp22
VIMPORTANT
p23
aVSENT
p24
asS'msg_cc'
p25
S'"Ludwig, Jens O" <jludwig@uchicago.edu>'
p26
sS'msg_bcc'
p27
Ns.