#include <iostream>

namespace {

class Greeting
{
public:
  explicit Greeting(const std::string& greeting = "Hello!")
    : m_greeting(greeting)
  {
  }

  operator std::string() const
  {
    return m_greeting;
  }

  Greeting& operator=(const std::string& greeting)
  {
    m_greeting = greeting;
  }

private:
  std::string m_greeting;
};

}

int main(int argc, char* argv[])
{
  std::cout << "Hello!" << std::endl;
  return 0;
}
