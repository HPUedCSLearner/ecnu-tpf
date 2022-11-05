!#include "../fortran/config.h"

subroutine maxnum(x,y)
  integer :: x,y
  if(x > y) then
    print *, x
  else
    print *, y
  end if
end subroutine maxnum

program main
 
  call  maxnum(3,4)

end program main

