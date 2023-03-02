#ifndef THREAD_POOL_H
#define THREAD_POOL_H

#include <mutex>
#include <queue>
#include <functional>
#include <future>
#include <thread>
#include <utility>
#include <vector>

template <typename T> // 模板类的实现，要放在一个文件中
class SafeQueue
{
private:
    std::queue<T> m_queue;
    std::mutex m_mutex; // 一个临界资源，一把锁;(正确编程，不会死锁); (两个临界资源，一把锁，会死锁)
public:
    SafeQueue() {}
    SafeQueue(SafeQueue &&other) {}
    ~SafeQueue() {}
    bool empty()
    {
        std::unique_lock<std::mutex> lock(m_mutex);
        return m_queue.empty();
    }
    int size()
    {
        std::unique_lock<std::mutex> lock(m_mutex);
        return m_queue.size();
    }
    void enQueue(T &t)
    {
        std::unique_lock<std::mutex> lock(m_mutex);
        m_queue.emplace(t);
    }
    bool deQueue(T &t)
    {
        std::unique_lock<std::mutex> lock(m_mutex);
        if (m_queue.empty()) {
            return false;
        }
        t = std::move(m_queue.front());
        m_queue.pop();
        return true;

    }
};

class ThreadPool
{
private:
    class ThreadWorker
    {
    private:
        int m_id;
        ThreadPool *m_pool;
    public:
        ThreadWorker(ThreadPool *pool, const int id) : m_pool(pool), m_id(id) {}
        void operator()()
        {
            std::function<void()> func;
            bool deQuequed;
            while (!m_pool->m_shutdown)
            {
                std::unique_lock<std::mutex> lock(m_pool->m_conditionalMutex);
                if (m_pool->m_taskSafeQue.empty()) {
                    m_pool->m_conditoinalLock.wait(lock);
                }
                deQuequed = m_pool->m_taskSafeQue.deQueue(func);
                if (deQuequed) {
                    func();
                }
            }
            
        }
    };
    bool m_shutdown;
    SafeQueue<std::function<void()>> m_taskSafeQue;
    std::vector<std::thread> m_threads;
    std::mutex m_conditionalMutex; // 一个线程池，一把锁
    std::condition_variable m_conditoinalLock; // 当临界资源超过1时,就要使用条件变量(进行休眠唤醒线程)
public:
    ThreadPool(const ThreadPool &) = delete; // 拷贝构造
    ThreadPool(ThreadPool &&) = delete;
    ThreadPool &operator=(const ThreadPool &) = delete; // 赋值构造
    ThreadPool &operator=(ThreadPool &&) = delete;

    ThreadPool(const int n_streads = 4)
    :m_threads(n_streads), m_shutdown(false) {}

    void init()
    {
        for (int i = 0; i < m_threads.size(); ++i) {
            m_threads.at(i) = std::thread(ThreadWorker(this, i));
        }
    }
    void shutdown()
    {
        m_shutdown = true;
        m_conditoinalLock.notify_all();
        for (int i = 0; i < m_threads.size(); ++i) {
            if (m_threads.at(i).joinable()) {
                m_threads.at(i).join();
            }
        }
    }
    template <typename F, typename... Args>
    auto submit(F &&f, Args &&...args) -> std::future<decltype(f(args...))>
    {
        std::function<decltype(f(args...))()> func = std::bind(std::forward<F>(f), std::forward<Args>(args)...);
        auto task_ptr = std::make_shared<std::packaged_task<decltype(f(args...))()>>(func);
        std::function<void()> wrapper_func = [task_ptr]() {
            (*task_ptr)();
        };
        m_taskSafeQue.enQueue(wrapper_func);
        m_conditoinalLock.notify_one();
        return task_ptr->get_future();
    }
};

#endif