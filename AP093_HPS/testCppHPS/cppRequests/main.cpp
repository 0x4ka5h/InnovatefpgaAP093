#include<iostream>
#include<cpr/cpr.h>
#include<nlohmann/json.hpp>

using namespace std;
using namespace cpr;

int main(){
	

	auto url = Url{"http://10.4.44.182:5000"};
	Session session;
	session.SetUrl(url);
	session.SetPayload(json{{"type_","owner"}});
	auto response = session.Get();
    
	Response res = Get(Url{"http://10.4.44.182:5000"});
	
	cout << res.text << endl;
}
