particlesJS('particles-js', //アニメーションを表示する要素(id)を指定する。同名のclassが存在する場合は動作しない
  {
    "particles": {
      //シェイプ数
      "number": {
        //要素内に表示するシェイプの数
        "value": 180,
        "density": {
          //シェイプ表示間隔設定
          "enable": true, //true:有効, false:無効
          //シェイプ表示間隔
          "value_area": 1000
        }
      },
      //シェイプ色
      "color": {
        "value": "#64bfe3"
      },
      //シェイプの設定
      "shape": {
        //シェイプ形
        "type": "circle", //設定値：circle, edge, triangle, polygon, star, image, 複数指定["circle", "triangle", "image"]
        //シェイプボーダー設定
        "stroke": {
          //ボーダー幅
          "width": 0,
          //ボーダー色
          "color": "#000000"
        },
        //シェイプの形でpolygonを指定した場合
        "polygon": {
          //ポリゴン角数指定
          "nb_sides": 6
        },
      },
      //シェイプ透過率指定
      "opacity": {
        //透過率指定
        "value": 0.4,
        //ランダム設定
        "random": true, //true:有効, false:無効
        //透過アニメーション設定
        "anim": {
          //アニメーション設定
          "enable": false, //true:有効, false:無効
          //アニメーション速度
          "speed": 0.7,
          //アニメーション最小透過率
          "opacity_min": 0.1,
          //アニメーション同期
          "sync": false //true:有効, false:無効
        }
      },
      //シェイプサイズ
      "size": {
        //シェイプサイズ指定
        "value": 2,
        //ランダムサイズ
        "random": true, //true:有効, false:無効
        //サイズアニメーション設定
        "anim": {
          //アニメーション設定
          "enable": true, //true:有効, false:無効
          //アニメーション速度
          "speed": 5,
          //アニメーション時のシェイプ最小サイズ,
          "size_min": 0.1,
          //アニメーション同期設定
          "sync": true //true:有効, false:無効
        }
      },
      //シェイプを線で繋ぐか
      "line_linked": {
        //線の設定
        "enable": true, //true:有効, false:無効
        //線の間隔
        "distance": 190,
        //線の色
        "color": "#64cef9",
        //線の透過率
        "opacity": 0.6,
        //線の幅
        "width": 1
      },
      //シェイプの動きの設定
      "move": {
        //動きを制御するか
        "enable": true, //true:有効, false:無効
        //動く速度
        "speed": 2,
        //動く方向
        "direction": "right", //none, top, top-right, right, bottom-right, bottom, bottom-left, left, top-left
        //ランダム設定
        "random": false, //true:有効, false:無効
        //静止状態にする
        "straight": false, //true:有効, false:無効
        //シェイプの動き
        "out_mode": "out", //ボックス内で動かす bounce ボックス外に逃がす out
        "attract": {
          "enable": false,
          "rotateX": 600,
          "rotateY": 1200
        }
      }
    },
    "interactivity": {
      "detect_on": "canvas",
      //マウスイベント設定
      "events": {
        //マウスオーバー時の処理
        "onhover": {
          "enable": false, //true:有効, false:無効
          "mode": "grab" //grad:付近のシェイプと線を繋ぐ, bubble:拡大, repulse:拒絶
        },
        //クリック時の処理処理
        "onclick": {
          //クリック時の処理
          "enable": false, //true:有効, false:無効
          //クリック時の処理の設定
          "mode": "push" //push:追加, remove:削除, bubble:拡大, repulse:拒絶
        },
        "resize": true
      },
      //以下でマウスイベント発生時の詳細値を設定
      "modes": {
        "grab": {
          "distance": 200,
          "line_linked": {
            "opacity": 1
          }
        },
        "bubble": {
          "distance": 400,
          "size": 40,
          "duration": 2,
          "opacity": 8,
          "speed": 3
        },
        "repulse": {
          "distance": 1
        },
        "push": {
          "particles_nb": 4
        },
        "remove": {
          "particles_nb": 2
        }
      }
    },
    //Retina Display対応
    "retina_detect": true, //true:有効, false:無効
    "resize": true //canvasのサイズ変更にわせて拡大縮小するか否か
  }
);