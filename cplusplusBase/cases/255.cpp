#include <iostream>         // 包含头文件。
#include <functional>
using namespace std;

struct Hero  {							// 英雄基类
	//virtual void show() { cout << "英雄释放了技能。\n"; }
	function<void()> m_callback;        // 用于绑定子类的成员函数。

	// 注册子类成员函数，子类成员函数没有参数。
	template<typename Fn, typename ...Args>
	void callback(Fn&& fn, Args&&...args) {
		m_callback = bind(forward<Fn>(fn), forward<Args>(args)...);
	}
	void show() { m_callback(); }   // 调用子类的成员函数。
};

struct XS :public Hero  {			// 西施派生类
	void show() { cout << "西施释放了技能。\n"; }
};

struct HX :public Hero  {			// 韩信派生类
	void show() { cout << "韩信释放了技能。\n"; }
};

int main()
{
	// 根据用户选择的英雄，施展技能。
	int id = 0;     // 英雄的id。
	cout << "请输入英雄（1-西施；2-韩信。）：";
	cin >> id;

	// 创建基类指针，将指向派生类对象，用基类指针调用派生类的成员函数。
	Hero* ptr = nullptr;

	if (id == 1) {            // 1-西施
		ptr = new XS;
		ptr->callback(&XS::show, static_cast<XS*>(ptr));  // 注册子类成员函数。
	}
	else if (id == 2) {     // 2-韩信
		ptr = new HX;
		ptr->callback(&HX::show, static_cast<HX*>(ptr));  // 注册子类成员函数。
	}

	if (ptr != nullptr) {
		ptr->show();		// 调用子类的成员函数。
		delete ptr;			// 释放派生类对象。
	}
}
