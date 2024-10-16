# cash_planner
 djangoを用いて、Web上にて家計簿としての基本的機能がある他、「AIパートナー」として家計簿のデータから無駄な出費といったサポートをしてくれるチャット形式の機能を追加する。 この「AIパートナー」では、GPT4o-miniのAPIキーを用いて出力するものとする。

## マイグレーション
`python manage.py makemigrations`</br>
`python manage.py migrate`</br>
**⚠マイグレーションエラーの場合**</br>
`python manage.py makemigrations cash_planner`</br>
`python manage.py migrate`</br>

## 環境構築
`python -m venv venv` 仮想環境を作成</br>
`.\venv\Scripts\activate` アクティベート</br>
`pip install django pandas matplotlib langchain langchain-community openai langchain_openai`
