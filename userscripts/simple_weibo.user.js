interested = document.getElementById('pl_content_homeInterest').getElementsByClassName('W_rightModule');

interested[0].style.display = 'none';

document.getElementsByClassName('nfTagB_group')[0].style.display = 'none';

to_hide = ['pl_content_pullylist', 'pl_content_medal', 'pl_content_mood', 'pl_content_promotetopic', 'pl_relation_recommendPopularUsers', 'pl_content_interestgroup', 'pl_content_topic', 'pl_content_allInOne', 'pl_common_noticeboard', 'pl_common_help', 'pl_common_feedback', 'pl_common_fun', 'ads_bottom_1'];

for (i in to_hide) {
    document.getElementById(to_hide[i]).style.display = 'none';
}


divs = document.getElementsByClassName('W_main_r')[0].getElementsByTagName('div');

for (i in divs) {
    var div = divs[i];
    console.log(div);

    if (div.id.match('^ad')) {
        div.style.display = 'none';
    }
}
