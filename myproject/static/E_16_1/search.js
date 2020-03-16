$(document).ready(function(){
    $("#btn_search").click(function(){
        document.getElementById("result").innerHTML = '抓取中.... 若期限過長，請稍後1分鐘!';
        var method =$("input[name='choose_type']:checked").val();
        var trend_type =$("input[name='trend_type']:checked").val();
		var checkbox_value = "";
		$(":checkbox").each(function () {
			var ischecked = $(this).is(":checked");
			if (ischecked) {
				checkbox_value += $(this).val() + "|";
			}
		});

        if(method=="one"){
            var stock_id = $("#stock_id").val();
            $.ajax({
                type: "GET",              //傳送方式
                url: "/stock/E_16_1_Py",    //傳送目的地
                data:{                   //要傳送的資料    
                    "stock_id":stock_id,
                    'trend_type':trend_type,
					'trade_type':checkbox_value
                },

                success: function (Data) {
                    $("#result").html(Data)
                },
                error: function (e) {
                    console.log(e);
                }
            });
        }
        else if(method=="all"){
			console.log(trend_type)
            $.ajax({
                type: "GET",              //傳送方式
                url: "/stock/E_16_1_Py",    //傳送目的地
                data:{                   //要傳送的資料    
                    "stock_id":"all",
                    "trend_type":trend_type,
                    'trade_type':checkbox_value
                },
                success: function (Data) {
                    $("#result").html(Data)
                },
                error: function (e) {
                    console.log(e);
                }
            });                          
        }
    })                
});