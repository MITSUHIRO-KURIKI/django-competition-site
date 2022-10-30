# django-competition-site(under development)

## What is this?
世界には優れた予測モデリングや分析手法のプラットフォーム(ex.kaggle, etc.)があり、多くのコンペティションが開催されています。また、それらの優れたアプリケーション上でプライベートなコンペティションを開催することができます。  
一方で、クローズドな環境でそうしたコンペティションを開催したいニーズ(外部への公開が禁止されている社内データを用いたコンペティションの開催など)があると考え、本アプリケーションを作成しました。  
**（アプリケーションは主要な機能を持ちますが、現時点で未完成です。）**
<small><blockquote>There are many excellent predictive modeling and analysis method platforms (ex.kaggle, etc.) in the world and many competitions are held on them. You can also hold private competitions on those excellent applications.  
On the other hand, we believe that there is a need to hold such competitions in a closed environment (e.g., competitions using internal company data that are not allowed to be disclosed to the outside world), so we created this application.  
**(The application has key features but is incomplete at this time.)**
</blockquote></small>

## way to use
* リポジトリをクローンし、仮想環境上でrequirements.txt をインストールします。
* .env ファイルの "SECRET_KEY" に任意のキーを入力します。（それ以外は必要に応じて記載します）
* Djangoアプリケーションをマイグレーションします（付属の ProjectStartBat.bat で一括処理も可能です）  
（使用には一般的なDjangoの経験が必要です。）
<small><blockquote>
* Clone the repository and install requirements.txt on the virtual environment.
* Enter any key in "SECRET_KEY" in the .env file. (Otherwise, enter any other key as needed)
* Migrate your Django application (you can also batch process with the included ProjectStartBat.bat)  
(General Django experience is required for use.)
</blockquote></small>

## Running in the Cloud
Google Cloud Platform での実行に対応していますが、デプロイには経験が必要です。  
また、セキュリティについて確認してください。オープンソースプログラムの実行と運用は自己責任でお願い致します。  
.env ファイルに必要な記述を行いデプロイできます。
<small><blockquote>
It supports running on Google Cloud, but requires experience to deploy.  
Also, please check about security. Please run and operate open source programs at your own risk.  
You can deploy it by making the necessary descriptions in the .env file.  
</blockquote></small>

## Other
アプリケーションは日本語で作成されています。  
オープンソースプログラムの実行と運用はすべて自己責任でお願い致します。  
本アプリケーションで使われる各種ライブラリのライセンスは本ライセンスには含まれません。各種ライブラリのライセンスに従って利用してください。  
本READMEの解釈は日本語が優先されます。  
<small><blockquote>
The application is written in Japanese.  
Please run and operate all open source programs at your own risk.  
Licenses for the various libraries used in this application are not included in this license. Please use them in accordance with the license of each library.  
The interpretation of the README takes precedence over the Japanese language.  
</blockquote></small>
