package dentaku;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.math.BigDecimal;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;

public class dentaku {
	static ArrayList<String> mlist = new ArrayList<String>();//macrolist
	static ArrayList<BigDecimal> rlist = new ArrayList<>();//resultlist
	static int seido = 3;
    public static void main(String args[]) {
	    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    	for(;;){
    		try{
    		System.out.print("input:");
    		String input= br.readLine();
    		if(input.indexOf("seido")>=0){
    			System.out.print("精度を入力:");
    			seido = Integer.parseInt(br.readLine());
    		}
    		else if(input.indexOf("makemacro")>=0){
    			makemacro(br);
    		}
    		else if(input.indexOf("showmacro")>=0){
    			showmacro();
    		}
    		else if(input.indexOf("deletemacro")>=0){
    			delmacro(br);
    		}
    		else if(input.indexOf("use m")>=0){
    			usemacro(br,Integer.parseInt(input.substring(input.indexOf("m")+1, input.length())));
    		}
    		else if(input.equals("end")){
    			System.out.println("終了します．");
    			break;
    		}
    		else{//計算式
    			calc(input);
    		}
    		}catch(Exception e){
    			System.out.println("エラー入力です");
    		}
    	}
    }

    private static void usemacro(BufferedReader br, int index) throws IOException {
    	String macro = mlist.get(index);
    	String input = new String();
    	System.out.println(macro);
    	String[] mstr = macro.split("\\s");
    	HashMap<String,String> vmap =  new HashMap<String,String>();
    	for(int i=0;i<mstr.length;i++){
    		if(mstr[i].indexOf("v")>=0){
    			String vname = mstr[i].substring(mstr[i].indexOf("v"),mstr[i].length());
    			if(!vmap.containsKey(vname)){
    				System.out.print(vname + ":");
    				vmap.put(vname, br.readLine());
    			}
    			input += vmap.get(vname) +" ";
    		}
    		else{
    			input += mstr[i]+" ";
    		}
    	}
    	System.out.println(input);
    	calc(input);
	}

	private static void delmacro(BufferedReader br) throws IOException {
    	System.out.print("削除したい番号を入力:");
    	int num = Integer.parseInt(br.readLine());
    	mlist.remove(num);
	}

	private static void makemacro(BufferedReader br) throws IOException{
    	System.out.print("マクロを作成:");
    	String mstr = br.readLine();
    	mlist.add(mstr);
    }

    private static void showmacro() {
    	if(mlist.size()==0){
    		System.out.println("作成されているマクロがありません");
    	}
    	else{
    		for(int i=0;i<mlist.size();i++){
    			System.out.println("m"+i+":"+mlist.get(i));
    		}
    	}
    }
	private static void calc(String input){
		try{
			int some = 0;
    		for(int i=0;i<input.length();i++){
    			if(input.charAt(i)== '&'){
    				some++;
    			}
    		}
    		String[] ilist = input.split("&");
    		for(int j =0;j<some+1;j++){
    			BigDecimal a = BigDecimal.valueOf(0);
    			BigDecimal b = BigDecimal.valueOf(0);
    			Boolean bool = true;
    			String[] str = ilist[j].split("\\s");
    			Deque<BigDecimal> que = new ArrayDeque<>();
    			for (int i = 0; i < str.length; i++) {
    				switch (str[i]) {
    				case "+":
    					a = que.pollFirst();
    	            	b = que.pollFirst();
    	            	que.addFirst(b.add(a));
    	            	break;
    				case "-":
    					a = que.pollFirst();
    					b = que.pollFirst();
    					que.addFirst(b.subtract(a));
    					break;
    				case "/":
    					a = que.pollFirst();
    					b = que.pollFirst();
    					que.addFirst(b.divide(a,seido,BigDecimal.ROUND_HALF_UP));
    					break;
    				case "*":
    					a = que.pollFirst();
    					b = que.pollFirst();
    					que.addFirst(b.multiply(a));
    					break;
    				default:
    					if(str[i].indexOf("x")!= -1){
    						int cnt = Integer.parseInt(str[i].substring(1,str[i].length()));
    						if(cnt>rlist.size()|| cnt<1){
    							bool = false;
    							System.out.println("存在しない過去の計算結果を利用しようとしています");
    							break;
    						}
    						else{
    							que.addFirst(rlist.get(rlist.size()-cnt));
    						}
    					}
    					else{
    					que.addFirst(new BigDecimal(str[i]));
    					}
    				}
    			}
    			if(bool){
        			System.out.print(ilist[j]+" = ");
    				BigDecimal result = que.pop().setScale(seido,BigDecimal.ROUND_HALF_UP);
    				rlist.add(result);
    				System.out.println(result);
    			}
    		}
		}catch(Exception e){
			System.out.println("計算式が間違っています");
		}
	}
}