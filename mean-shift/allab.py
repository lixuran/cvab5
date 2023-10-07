///1

#include <iostream>
#include <vector>
#include <map>

#include <CGAL/QP_models.h>
#include <CGAL/QP_functions.h>
#include <CGAL/Gmpz.h>
typedef int IT;
typedef CGAL::Gmpz ET;

typedef CGAL::Quadratic_program<IT> Program;
typedef CGAL::Quadratic_program_solution<ET> Solution;

int main()
{
  std::ios_base::sync_with_stdio(false);
  int t;
  std::cin>>t;
  for (int i=0;i<t;i++)
  {
    int n,m,h,w;
    int x,y;
    
    std::cin>>n>>m>>h>>w;
    int pos_new[n][2];
    int pos_old[m][2];
    
    for (int j=0;j<n;j++)
    {
      std::cin>>x>>y;
      pos_new[j][0]=x;
      pos_new[j][1]=y;
    }
    for (int j=0;j<m;j++)
    {
      std::cin>>x>>y;
      pos_old[j][0]=x;
      pos_old[j][1]=y;
    }
    //init 
    Program lp (CGAL::SMALLER,true,1,false,0);
    // we cant be naming abc since we dont know how many variable there are.
    
    //start adding constraints
    long counter =0;
    for (int j=0;j<n;j++)
    {
      lp.set_l(j,true,1);
      for (int k=j+1;k<n;k++)
      {
        
        int disx = std::abs(pos_new[j][0] - pos_new[k][0]);
        int disy = std::abs(pos_new[j][1] - pos_new[k][1]);
        int dis =0;
        if (disx*h>=disy*w)
        {
          dis = 2*disx;
        }
        else
        {
          dis =2*disy; 
        }
        //std::cout<<dis<<" dis\n";
       // std::cout<<"x y "<<disx<<" "<<disy<<"\n";
        for (int iter=0;iter<n;iter++)
        {
          if(iter== j or iter ==k)
          {
            if (disx*h>=disy*w)
            {
              lp.set_a(iter,counter,w);
            }
            else
            {
              lp.set_a(iter,counter,h);
            }
          }
          else
          {
            lp.set_a(iter,counter,0);
          }
          
        }
        //lp.set_a(n,counter,0);
        lp.set_b(counter,dis);
        counter++;
        
        // for (int iter=0;iter<n;iter++)
        // {
        //   if(iter== j or iter ==k)
        //   {
        //     lp.set_a(iter,counter,h/2);
        //   }
        //   else
        //   {
        //     lp.set_a(iter,counter,0);
        //   }
          
        // }
        // lp.set_a(n,counter,0);
        // lp.set_b(counter,disy);
        // counter++;
      }
    }
    for (int j=0;j<n;j++)
    {
      for (int k=0;k<m;k++)
      {
        
        int disx = std::abs(pos_new[j][0] - pos_old[k][0]);
        int disy = std::abs(pos_new[j][1] - pos_old[k][1]);
        int dis =0;
        if (disx*h>=disy*w)
        {
          dis = 2*disx;
        }
        else
        {
          dis =2*disy; 
        }
       // std::cout<<dis<<" dis\n";
        //std::cout<<"x y v2 "<<disx<<" "<<disy<<"\n";
        for (int iter=0;iter<n;iter++) //copyed to do check this
        {
          if(iter== j)
          {
            if (disx*h>=disy*w)
            {
              lp.set_a(iter,counter,w);
            }
            else
            {
              lp.set_a(iter,counter,h);
            }
          }
          else
          {
            lp.set_a(iter,counter,0);
          }
          
        }
        //lp.set_a(n,counter,w/2+h/2);
        if (disx*h>=disy*w)
        {
          lp.set_b(counter,dis-w);
        }
        else
        {
          lp.set_b(counter,dis-h);
        }
        //lp.set_b(counter,dis-1);
        counter++;
        // for (int iter=0;iter<n;iter++) //copyed to do check this
        // {
        //   if(iter== j)
        //   {
        //     lp.set_a(iter,counter,h/2);
        //   }
        //   else
        //   {
        //     lp.set_a(iter,counter,0);
        //   }
          
        // }
        // lp.set_a(n,counter,h/2);
        // lp.set_b(counter,disy);
        // counter++;
        
      }
    }
    //add objective
    for (int j=0;j<n;j++)
    {
      lp.set_c(j,-2*h-2*w);
    
    }
    
    lp.set_c0(0);
    //add bounds
    
    //solve
    Solution s = CGAL::solve_linear_program(lp,ET());
    assert(s.solves_linear_program(lp));
    //print
   
    double a =s.objective_value().numerator().to_double();
    double b =s.objective_value().denominator().to_double();
    std::cout<<(int)std::ceil(-a/b)<<"\n";
  
    // typedef Solution::Variable_value_iterator SVI;
    // for (auto opt=s.variable_values_begin();opt<s.variable_values_end();++opt)
    // {
    //   CGAL::Quotient<ET> res= *opt;
    //   std::cout<<res.numerator()<<"/"<<res.denominator()<<"\n";
    // }
    
  }
  
  
  
  
  
  
  
  
  
  return 0;
}