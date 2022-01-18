class Cookies {
    constructor () {}

    get(name){
        let matches = document.cookie.match(new RegExp(
            "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
        ));
        return matches ? decodeURIComponent(matches[1]) : undefined;
    }

    set(name, value, options = {}) {
        options = {
            path: '/',
            ...options
        };        
        let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);        
        for (let optionKey in options) {
            updatedCookie += "; " + optionKey;
            let optionValue = options[optionKey];
            if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
            }
        }        
        document.cookie = updatedCookie;
    }

    delete(name) {
        this.set(name, "", {'max-age': -1});
    }
}

class Table {
    constructor(table_id){
      this.table_id = table_id;    
      this.refresh()
    }    

    refresh(){
      $("#"+ this.table_id +"-pagination").empty();
      $("#"+ this.table_id +"-pagination").append('<li class="page-item"><a class="page-link" href="#" onclick="table.previousPage()">&laquo;</a></li>');
      this.index = 1;
      this.page_count = 1;
      var table_id__ = this.table_id;
      var index__ = this.index;
      var page_count__ = this.page_count;
      $("#"+ table_id__ +"-pagination").append('<li class="page-item"><a class="page-link" href="#" onclick="table.openPage('+page_count__+')">'+page_count__+'</a></li>');
      $("#" + this.table_id + ">tbody>tr").each(function(index, element){
        if (index + 1 > index__ * 10) {
          $(this).css('display', 'none');
        }
        if (index % 10 === 1) {
          page_count__++;
          $("#"+ table_id__ +"-pagination").append('<li class="page-item"><a class="page-link" href="#" onclick="table.openPage('+page_count__+')">'+page_count__+'</a></li>');
        }
      });    
      this.index = index__;
      this.page_count = page_count__;
      $("#"+ this.table_id +"-pagination").append('<li class="page-item"><a class="page-link" href="#" onclick="table.nextPage()">&raquo;</a></li>');
    }

    openPage(page_id){
      if (page_id < 1 || page_id > this.page_count){return false}

      var index__ = this.index;
      var page_count__ = this.page_count;

      $("#" + this.table_id + ">tbody>tr").each(function(index, element){
        if (index >= page_id * 10 - 10 && index < page_id * 10) {
          $(this).css('display', 'table-row');
        } else {
          $(this).css('display', 'none');
        }
        index__ = page_id;        
      });
      this.index = index__;
      return true;
    }

    nextPage(){
      return this.openPage(this.index + 1);
    }

    previousPage(){
      return this.openPage(this.index - 1);
    }
    
    search(input_id){
      var phrase = document.getElementById(input_id);
      var table = document.getElementById(this.table_id);
      var regPhrase = new RegExp(phrase.value, 'i');
      var flag = false;
      for (var i = 1; i < table.rows.length; i++) {
          flag = false;
          for (var j = table.rows[i].cells.length - 1; j >= 0; j--) {
              flag = regPhrase.test(table.rows[i].cells[j].innerHTML);
              if (flag) break;
          }
          if (flag) {
              table.rows[i].style.display = "";
          } else {
              table.rows[i].style.display = "none";
          }
      }
      if ($("#" + input_id).val() === ""){
        this.refresh()
      }
    }
}

var cookies = new Cookies();