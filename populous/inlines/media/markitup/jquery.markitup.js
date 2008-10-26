// ----------------------------------------------------------------------------
// markItUp! Universal MarkUp Engine, JQuery plugin
// v 1.1.1 beta
// Dual licensed under the MIT and GPL licenses.
// ----------------------------------------------------------------------------
// Copyright (C) 2007-2008 Jay Salvat
// http://markitup.jaysalvat.com/
// ----------------------------------------------------------------------------
eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('(3($){$.2e.U=3(f,g){E k,u,z,J;u=z=J=l;k={B:\'\',16:\'\',R:\'\',1x:\'\',1W:m,2A:\'2x\',1w:\'~/3s/1G.12\',1d:\'\',2b:\'27\',1r:m,1D:\'\',1B:\'\',1A:{},1Z:{},1X:{},1V:{},2H:[{}]};$.W(k,f,g);2(!k.R){$(\'3B\').1f(3(a,b){1Q=$(b).14(0).3q.3n(/(.*)3k\\.3i(\\.3d)?\\.3a$/);2(1Q!==2h){k.R=1Q[1]}})}4 H.1f(3(){E d,q,19,15,o,D,K,O,Z,1y,v,1v,L,18;d=$(H);q=H;19=[];18=l;15=o=0;D=-1;k.1d=1h(k.1d);k.1w=1h(k.1w);3 1h(a,b){2(b){4 a.T(/("|\')~\\//g,"$1"+k.R)}4 a.T(/^~\\//,k.R)}3 2F(){B=\'\';16=\'\';2(k.B){B=\'B="\'+k.B+\'"\'}6 2(d.1U("B")){B=\'B="U\'+(d.1U("B").2C(0,1).3D())+(d.1U("B").2C(1))+\'"\'}2(k.16){16=\'N="\'+k.16+\'"\'}d.1T(\'<w \'+16+\'"></w>\');d.1T(\'<w \'+B+\' N="U"></w>\');d.1T(\'<w N="3A"></w>\');d.2w("2v");Z=$(\'<w N="3x"></w>\').2u(d);$(1P(k.2H)).1O(Z);1y=$(\'<w N="3v"></w>\').1C(d);2(k.1r===m&&$.1a.3r!==m){1r=$(\'<w N="3p"></w>\').1C(d).1c("3l",3(e){E h=d.2c(),y=e.2i,1n,1l;1n=3(e){d.2d("2c",37.36(20,e.2i+h-y)+"34");4 l};1l=3(e){$("12").1J("2k",1n).1J("1p",1l);4 l};$("12").1c("2k",1n).1c("1p",1l)});1y.2q(1r)}d.26(1N).2W(1N);d.1c("1E",3(e,a){2(a.1j!==l){14()}2(q===$.U.23){V(a)}});d.1g(3(){$.U.23=H})}3 1P(b){E c=$(\'<X></X>\'),i=0;$(\'A:21 > X\',c).2d(\'2O\',\'p\');$(b).1f(3(){E a=H,t=\'\',1k,A,j;1k=(a.11)?(a.1Y||\'\')+\' [3O+\'+a.11+\']\':(a.1Y||\'\');11=(a.11)?\'2M="\'+a.11+\'"\':\'\';2(a.2L){A=$(\'<A N="3N">\'+(a.2L||\'\')+\'</A>\').1O(c)}6{i++;2K(j=19.5-1;j>=0;j--){t+=19[j]+"-"}A=$(\'<A N="2J 2J\'+t+(i)+\' \'+(a.3M||\'\')+\'"><a 3L="" \'+11+\' 1k="\'+1k+\'">\'+(a.1Y||\'\')+\'</a></A>\').1c("3K",3(){4 l}).2I(3(){4 l}).1p(3(){2(a.2G){3J(a.2G)()}V(a);4 l}).21(3(){$(\'> X\',H).3I();$(C).3H(\'2I\',3(){$(\'X X\',Z).2E()})},3(){$(\'> X\',H).2E()}).1O(c);2(a.2D){19.3G(i);$(A).2w(\'3F\').2q(1P(a.2D))}}});19.3E();4 c}3 2B(c){2(c){c=c.3C();c=c.T(/\\(\\!\\(([\\s\\S]*?)\\)\\!\\)/g,3(x,a){E b=a.1S(\'|!|\');2(J===m){4(b[1]!==2z)?b[1]:b[0]}6{4(b[1]===2z)?"":b[0]}});c=c.T(/\\[\\!\\[([\\s\\S]*?)\\]\\!\\]/g,3(x,a){E b=a.1S(\':!:\');2(18===m){4 l}1R=3z(b[0],(b[1])?b[1]:\'\');2(1R===2h){18=m}4 1R});4 c}4""}3 F(a){2($.3y(a)){a=a(O)}4 2B(a)}3 1e(a){G=F(K.G);17=F(K.17);P=F(K.P);M=F(K.M);2(P!==""){p=G+P+M}6 2(8===\'\'&&17!==\'\'){p=G+17+M}6{p=G+(a||8)+M}4{p:p,G:G,P:P,17:17,M:M}}3 V(a){E b,j,n,i;O=K=a;14();$.W(O,{1u:"",R:k.R,q:q,8:(8||\'\'),o:o,u:u,z:z,J:J});F(k.1D);F(K.1D);2(u===m&&z===m){F(K.3w)}$.W(O,{1u:1});2(u===m&&z===m){Q=8.1S(/\\r?\\n/);2K(j=0,n=Q.5,i=0;i<n;i++){2($.3u(Q[i])!==\'\'){$.W(O,{1u:++j,8:Q[i]});Q[i]=1e(Q[i]).p}6{Q[i]=""}}7={p:Q.3t(\'\\n\')};Y=o;b=7.p.5+(($.1a.2r)?n:0)}6 2(u===m){7=1e(8);Y=o+7.G.5;b=7.p.5-7.G.5-7.M.5;b-=1q(7.p)}6 2(z===m){7=1e(8);Y=o;b=7.p.5;b-=1q(7.p)}6{7=1e(8);Y=o+7.p.5;b=0;Y-=1q(7.p)}2((8===\'\'&&7.P===\'\')){D+=1M(7.p);Y=o+7.G.5;b=7.p.5-7.G.5-7.M.5;D=d.I().1b(o,d.I().5).5;D-=1M(d.I().1b(0,o))}$.W(O,{o:o,15:15});2(7.p!==8&&18===l){2o(7.p);1L(Y,b)}6{D=-1}14();$.W(O,{1u:\'\',8:8});2(u===m&&z===m){F(K.3o)}F(K.1B);F(k.1B);2(v&&k.1W){1I()}z=J=u=18=l}3 1M(a){2($.1a.2r){4 a.5-a.T(/\\n*/g,\'\').5}4 0}3 1q(a){2($.1a.2n){4 a.5-a.T(/\\r*/g,\'\').5}4 0}3 2o(a){2(C.8){E b=C.8.1F();b.2m=a}6{d.I(d.I().1b(0,o)+a+d.I().1b(o+8.5,d.I().5))}}3 1L(a,b){2(q.2l){1i=q.2l();1i.3j(m);1i.2a(\'1H\',a);1i.3h(\'1H\',b);1i.3f()}6 2(q.2f){q.2f(a,a+b)}q.1m=15;q.1g()}3 14(){q.1g();15=q.1m;2(C.8){8=C.8.1F().2m;2($.1a.2n){E a=C.8.1F(),1o=a.3c();1o.3b(q);o=-1;39(1o.38(a)){1o.2a(\'1H\');o++}}6{o=q.2j}}6{o=q.2j;8=d.I().1b(o,q.3e)}4 8}3 1G(){2(!v||v.35){2(k.1x){v=3g.2g(\'\',\'1G\',k.1x)}6{L=$(\'<2N N="33"></2N>\');2(k.2A==\'2x\'){L.1C(1y)}6{L.2u(Z)}v=L[L.5-1].32||31[L.5-1]}}6 2(J===m){2(L){L.3m()}v.29();v=L=l}2(!k.1W){1I()}}3 1I(){2(v.C){30{1K=v.C.28.1m}2Z(e){1K=0}v.C.2g();v.C.2Y(2p());v.C.29();v.C.28.1m=1K}2(k.1x){v.1g()}}3 2p(){2(k.1d!==\'\'){$.2y({25:\'2X\',2s:l,2t:k.1d,27:k.2b+\'=\'+2V(d.I()),24:3(a){12=1h(a,1)}})}6{2(!1v){$.2y({2s:l,2t:k.1w,24:3(a){1v=1h(a,1)}})}12=1v.T(/<!-- 2U -->/g,d.I())}4 12}3 1N(e){z=e.z;J=e.J;u=(!(e.J&&e.u))?e.u:l;2(e.25===\'26\'){2(u===m){A=$("a[2M="+2T.2S(e.1t)+"]",Z).1s(\'A\');2(A.5!==0){u=l;A.2R(\'1p\');4 l}}2(e.1t===13||e.1t===10){2(u===m){u=l;V(k.1X);4 k.1X.1z}6 2(z===m){z=l;V(k.1Z);4 k.1Z.1z}6{V(k.1A);4 k.1A.1z}}2(e.1t===9){2(D!==-1){14();D=d.I().5-D;1L(D,0);D=-1;4 l}6{V(k.1V);4 k.1V.1z}}}}2F()})};$.2e.2Q=3(){4 H.1f(3(){$$=$(H).1J().2P(\'2v\');$$.1s(\'w\').1s(\'w.U\').1s(\'w\').P($$)})};$.U=3(a){E b={1j:l};$.W(b,a);2(b.1j){4 $(b.1j).1f(3(){$(H).1g();$(H).22(\'1E\',[b])})}6{$(\'q\').22(\'1E\',[b])}}})(3P);',62,238,'||if|function|return|length|else|string|selection|||||||||||||false|true||caretPosition|block|textarea||||ctrlKey|previewWindow|div|||shiftKey|li|id|document|caretOffset|var|prepare|openWith|this|val|altKey|clicked|iFrame|closeWith|class|hash|replaceWith|lines|root||replace|markItUp|markup|extend|ul|start|header||key|html||get|scrollPosition|nameSpace|placeHolder|abort|levels|browser|substring|bind|previewParserPath|build|each|focus|localize|range|target|title|mouseUp|scrollTop|mouseMove|rangeCopy|mouseup|fixIeBug|resizeHandle|parent|keyCode|line|template|previewTemplatePath|previewInWindow|footer|keepDefault|onEnter|afterInsert|insertAfter|beforeInsert|insertion|createRange|preview|character|refreshPreview|unbind|sp|set|fixOperaBug|keyPressed|appendTo|dropMenus|miuScript|value|split|wrap|attr|onTab|previewAutoRefresh|onCtrlEnter|name|onShiftEnter||hover|trigger|focused|success|type|keydown|data|documentElement|close|moveStart|previewParserVar|height|css|fn|setSelectionRange|open|null|clientY|selectionStart|mousemove|createTextRange|text|msie|insert|renderPreview|append|opera|async|url|insertBefore|markItUpEditor|addClass|after|ajax|undefined|previewPosition|magicMarkups|substr|dropMenu|hide|init|call|markupSet|click|markItUpButton|for|separator|accesskey|iframe|display|removeClass|markItUpRemove|triggerHandler|fromCharCode|String|content|encodeURIComponent|keyup|POST|write|catch|try|frame|contentWindow|markItUpPreviewFrame|px|closed|max|Math|inRange|while|js|moveToElementText|duplicate|pack|selectionEnd|select|window|moveEnd|markitup|collapse|jquery|mousedown|remove|match|afterMultiInsert|markItUpResizeHandle|src|safari|templates|join|trim|markItUpFooter|beforeMultiInsert|markItUpHeader|isFunction|prompt|markItUpContainer|script|toString|toUpperCase|pop|markItUpDropMenu|push|one|show|eval|contextmenu|href|className|markItUpSeparator|Ctrl|jQuery'.split('|'),0,{}))