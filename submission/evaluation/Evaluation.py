# python module
import numpy as np
import pandas as pd
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
    mean_squared_error,
    mean_squared_log_error,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    fbeta_score,
    log_loss,
    roc_auc_score,
    cohen_kappa_score,
)
from django.conf import settings
from google.cloud import storage
from io import BytesIO
import gc

def Evaluation(submit_file, answer_file, metrics, target_cols_name):
    public_score = None
    private_score = None

    # データ読込
    submit_file_df = pd.read_csv(submit_file)
    if settings.USE_GCS:
        gcs = storage.Client()
        client = gcs.from_service_account_json(settings.GS_CREDENTIALS_JSON)
        bucket = client.bucket(settings.GS_BUCKET_NAME)
        blob = bucket.blob(answer_file.name)
        answer_file_df = pd.read_csv(BytesIO(blob.download_as_string()))
    else:
        answer_file_df = pd.read_csv(answer_file)

    # public 用データの抽出
    public_score_ix = answer_file_df[answer_file_df.division_public_or_private == 'public'].index
    public_answer_file_df = answer_file_df.iloc[public_score_ix].copy()
    public_submit_file_df = submit_file_df.iloc[public_score_ix].copy()

    # 正解/予測 の対象のカラム名
    target_cols_name = target_cols_name.replace(' ','').replace('　','').split(',')

    # public data
    public_y_true = public_answer_file_df[target_cols_name]
    public_y_pred = public_submit_file_df[target_cols_name]
    
    # private data
    private_y_true = answer_file_df[target_cols_name]
    private_y_pred = submit_file_df[target_cols_name]

    # マルチカラムの場合には np.array に変換
    if len(target_cols_name) > 1:
        public_y_true = np.array(public_y_true)
        public_y_pred = np.array(public_y_pred)
        private_y_true = np.array(private_y_true)
        private_y_pred = np.array(private_y_pred)

    del submit_file_df, answer_file_df
    del public_answer_file_df, public_submit_file_df
    gc.collect()

    # metrics に応じた評価関数の実行
    try:
        public_score, private_score = Metrics(public_y_true, public_y_pred, private_y_true, private_y_pred, metrics)
    except:
        public_score = None
        private_score = None

    # 小数点丸め
    public_score = np.round(public_score, decimals=5)
    private_score = np.round(private_score, decimals=5)

    return public_score, private_score


def Metrics(public_y_true, public_y_pred, private_y_true, private_y_pred, metrics):

    ####################
    # 回帰モデルの評価指標
    ####################

    # 決定係数 (R^2)
    if metrics == 'R2_score':
        public_score = r2_score(public_y_true, public_y_pred)
        private_score = r2_score(private_y_true, private_y_pred)

    # 平均絶対誤差 (MAE)
    if metrics == 'Mean_absolute_error':
        public_score = mean_absolute_error(public_y_true, public_y_pred)
        private_score = mean_absolute_error(private_y_true, private_y_pred)
    
    # 平均二乗誤差 (MSE)
    if metrics == 'Mean_squared_error':
        public_score = mean_squared_error(public_y_true, public_y_pred)
        private_score = mean_squared_error(private_y_true, private_y_pred)
    
    # 二乗平均平方根誤差 (RMSE)
    if metrics == 'Root_mean_squared_error':
        public_score = np.sqrt(mean_squared_error(public_y_true, public_y_pred))
        private_score = np.sqrt(mean_squared_error(private_y_true, private_y_pred))
    
    # MSLE
    if metrics == 'Mean_squared_log_error':
        public_score = mean_squared_log_error(public_y_true, public_y_pred)
        private_score = mean_squared_log_error(private_y_true, private_y_pred)
    
    # RMSLE
    if metrics == 'Root_mean_squared_log_error':
        public_score = np.sqrt(mean_squared_log_error(public_y_true, public_y_pred))
        private_score = np.sqrt(mean_squared_log_error(private_y_true, private_y_pred))

    ####################
    # 分類モデルの評価指標
    ####################

    # 正解率 (Accuracy)
    if metrics == 'Accuracy_score':
        public_score = accuracy_score(public_y_true, public_y_pred)
        private_score = accuracy_score(private_y_true, private_y_pred)
    
    # 誤答率 (Error)
    if metrics == 'Error_rate':
        public_score = accuracy_score(public_y_true, public_y_pred)
        public_score = 1 -public_score
        private_score = accuracy_score(private_y_true, private_y_pred)
        private_score = 1 - private_score
    
    # 精度 (Precision)
    if metrics == 'Precision_score':
        public_score = precision_score(public_y_true, public_y_pred)
        private_score = precision_score(private_y_true, private_y_pred)
    
    #検出率 (Recall)
    if metrics == 'Recall_score':
        public_score = recall_score(public_y_true, public_y_pred)
        private_score = recall_score(private_y_true, private_y_pred)
    
    # F1
    if metrics == 'F1_score':
        public_score = f1_score(public_y_true, public_y_pred, average='binary')
        private_score = f1_score(private_y_true, private_y_pred, average='binary')
    
    # F1_mean
    if metrics == 'F1_score_mean':
        public_score = f1_score(public_y_true, public_y_pred, average='samples')
        private_score = f1_score(private_y_true, private_y_pred, average='samples')
    
    # F1_macro
    if metrics == 'F1_score_macro':
        public_score = f1_score(public_y_true, public_y_pred, average='macro')
        private_score = f1_score(private_y_true, private_y_pred, average='macro')
    
    # F1_micro
    if metrics == 'F1_score_micro':
        public_score = f1_score(public_y_true, public_y_pred, average='micro')
        private_score = f1_score(private_y_true, private_y_pred, average='micro')
    
    # F1_weighted
    if metrics == 'F1_score_weighted':
        public_score = f1_score(public_y_true, public_y_pred, average='weighted')
        private_score = f1_score(private_y_true, private_y_pred, average='weighted')
    
    # F1_none (multilabel classification)
    if metrics == 'F1_score_none':
        public_score = f1_score(public_y_true, public_y_pred, average=None)
        private_score = f1_score(private_y_true, private_y_pred, average=None)
    
    # F0.5
    if metrics == 'F0.5_score':
        public_score = fbeta_score(public_y_true, public_y_pred, beta=0.5, average='binary')
        private_score = fbeta_score(private_y_true, private_y_pred, beta=0.5, average='binary')

    # F0.5_mean
    if metrics == 'F0.5_score_mean':
        public_score = fbeta_score(public_y_true, public_y_pred, beta=0.5, average='samples')
        private_score = fbeta_score(private_y_true, private_y_pred, beta=0.5, average='samples')

    # F0.5_macro
    if metrics == 'F0.5_score_macro':
        public_score = fbeta_score(public_y_true, public_y_pred, beta=0.5, average='macro')
        private_score = fbeta_score(private_y_true, private_y_pred, beta=0.5, average='macro')

    # F0.5_micro
    if metrics == 'F0.5_score_micro':
        public_score = fbeta_score(public_y_true, public_y_pred, beta=0.5, average='micro')
        private_score = fbeta_score(private_y_true, private_y_pred, beta=0.5, average='micro')

    # F0.5_weighted
    if metrics == 'F0.5_score_weighted':
        public_score = fbeta_score(public_y_true, public_y_pred, beta=0.5, average='weighted')
        private_score = fbeta_score(private_y_true, private_y_pred, beta=0.5, average='weighted')
    
    # F0.5_none (multilabel classification)
    if metrics == 'F0.5_score_none':
        public_score = fbeta_score(public_y_true, public_y_pred, beta=0.5, average=None)
        private_score = fbeta_score(private_y_true, private_y_pred, beta=0.5, average=None)
    
    # F2
    if metrics == 'F2_score':
        public_score = fbeta_score(public_y_true, public_y_pred, beta=2, average='binary')
        private_score = fbeta_score(private_y_true, private_y_pred, beta=2, average='binary')
    
    # F2_mean
    if metrics == 'F2_score_mean':
        public_score = fbeta_score(public_y_true, public_y_pred, beta=2, average='samples')
        private_score = fbeta_score(private_y_true, private_y_pred, beta=2, average='samples')

    # F2_macro
    if metrics == 'F2_score_macro':
        public_score = fbeta_score(public_y_true, public_y_pred, beta=2, average='macro')
        private_score = fbeta_score(private_y_true, private_y_pred, beta=2, average='macro')

    # F2_micro
    if metrics == 'F2_score_micro':
        public_score = fbeta_score(public_y_true, public_y_pred, beta=2, average='micro')
        private_score = fbeta_score(private_y_true, private_y_pred, beta=2, average='micro')

    # F2_weighted
    if metrics == 'F2_score_weighted':
        public_score = fbeta_score(public_y_true, public_y_pred, beta=2, average='weighted')
        private_score = fbeta_score(private_y_true, private_y_pred, beta=2, average='weighted')

    # F2_none (multilabel classification)
    if metrics == 'F2_score_none':
        public_score = fbeta_score(public_y_true, public_y_pred, beta=2, average=None)
        private_score = fbeta_score(private_y_true, private_y_pred, beta=2, average=None)

    # log_loss
    if metrics == 'Log_loss':
        public_score = log_loss(public_y_true, public_y_pred)
        private_score = log_loss(private_y_true, private_y_pred)

    # roc_auc_score
    if metrics == 'Roc_auc_score':
        public_score = roc_auc_score(public_y_true, public_y_pred)
        private_score = roc_auc_score(private_y_true, private_y_pred)

    # roc_auc_score_Multiclass
    if metrics == 'Roc_auc_score_Multiclass':
        public_score = roc_auc_score(public_y_true, public_y_pred, multi_class='ovr')
        private_score = roc_auc_score(private_y_true, private_y_pred, multi_class='ovr')

    # roc_auc_score_Multilabel
    if metrics == 'Roc_auc_score_Multilabel':
        public_score = roc_auc_score(public_y_true, public_y_pred, average=None)
        private_score = roc_auc_score(private_y_true, private_y_pred, average=None)

    # quadratic_weighted_kappa
    if metrics == 'Quadratic_weighted_kappa':
        public_score = cohen_kappa_score(public_y_true, public_y_pred, weights='quadratic')
        private_score = cohen_kappa_score(private_y_true, private_y_pred, weights='quadratic')

    ####################
    # レコメンデーションの評価指標
    ####################
    # MAP@K
    if metrics == 'MAP@K':

        def apk(y_i_true, y_i_pred):
            assert (len(y_i_pred) <= K)
            assert (len(np.unique(y_i_pred)) == len(y_i_pred))
            sum_precision = 0.0
            num_hits = 0.0
            for i, p in enumerate(y_i_pred):
                if p in y_i_true:
                    num_hits += 1
                    precision = num_hits / (i + 1)
                    sum_precision += precision
            return sum_precision / min(len(y_i_true), K)

        def mapk(y_true, y_pred):
            return np.mean([apk(y_i_true, y_i_pred) for y_i_true, y_i_pred in zip(y_true, y_pred)])

        public_score = mapk(public_y_true, public_y_pred)
        private_score = mapk(private_y_true, private_y_pred)


    ####################
    # カスタム評価指標
    ####################

    # if metrics == '###カスタム評価指標名###':
    #     def CUSTOM_METRICS(y_true, y_pred):
    #         *** ***
    #         return score
    #     public_score = CUSTOM_METRICS(public_y_true, public_y_pred)
    #     private_score = CUSTOM_METRICS(private_y_true, private_y_pred)

    return public_score, private_score